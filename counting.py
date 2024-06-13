import cv2
import numpy as np

# กำหนด ROI (Region of Interest)
roi_x, roi_y, roi_w, roi_h = 100, 100, 400, 300  # ตัวอย่างค่า ROI

# โหลดไฟล์โมเดล YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# โหลดชื่อวัตถุ
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# โหลดวิดีโอจากกล้องเว็บแคม (0 คือค่าเริ่มต้นของกล้องเว็บแคม)
cap = cv2.VideoCapture(0)
#...

# ฟังก์ชั่นตรวจจับวัตถุ
def detect_objects(frame):
    height, width, channels = frame.shape

    # สร้าง blob จากภาพ
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # ประมวลผลผลลัพธ์
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # ตรวจพบวัตถุ
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    result = []
    for i in range(len(boxes)):
        if i in indexes:
            box = boxes[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            result.append((x, y, w, h, class_ids[i]))

    return result

# ตัวแปรนับจำนวนวัตถุที่ผ่านเข้าไปในกรอบ ROI
object_counter = 0

# ตัวแปรเก็บการติดตามวัตถุ
trackers = []
object_ids = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ตัดกรอบ ROI
    roi_frame = frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]

    # ตรวจจับวัตถุในกรอบ ROI
    objects = detect_objects(roi_frame)

    # อัพเดต trackers
    new_trackers = []
    new_object_ids = []
    for tracker, obj_id in zip(trackers, object_ids):
        success, box = tracker.update(roi_frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            if x > 0 and y > 0 and x + w < roi_w and y + h < roi_h:
                new_trackers.append(tracker)
                new_object_ids.append(obj_id)
            else:
                object_counter += 1  # เพิ่มตัวนับเมื่อวัตถุออกจากกรอบ
        else:
            object_counter += 1  # เพิ่มตัวนับเมื่อการติดตามล้มเหลว

    trackers = new_trackers
    object_ids = new_object_ids

    # วาดกรอบและชื่อวัตถุ
    for tracker in trackers:
        success, box = tracker.update(roi_frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # ตรวจจับวัตถุใหม่และเพิ่มเข้าไปใน trackers
    for (x, y, w, h, class_id) in objects:
        label = str(classes[class_id])
        new_tracker = cv2.TrackerMIL_create()
        new_tracker.init(roi_frame, (x, y, w, h))
        trackers.append(new_tracker)
        object_ids.append(len(trackers))
        cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(roi_frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # แสดงกรอบ ROI บนเฟรมหลัก
    frame[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w] = roi_frame
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_w, roi_y+roi_h), (255, 0, 0), 2)

    # แสดงจำนวนวัตถุที่ผ่านกรอบ ROI
    cv2.putText(frame, f"Count: {object_counter}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # แสดงผลลัพธ์
    cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
