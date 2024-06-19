import cv2
from ultralytics import YOLO, solutions

class ObjectCounter:
    def __init__(self, video_path=None, output_path="output.avi", yolo_model_path="yolov8n.pt", line_points=None, classes_to_count=None, display_video=True, use_webcam=False):
        # โหลดโมเดล YOLO ที่ฝึกไว้ล่วงหน้า
        self.model = YOLO(yolo_model_path)

        # เปิดไฟล์วิดีโอหรือกล้องเว็บแคม
        if use_webcam:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(video_path)
        
        assert self.cap.isOpened(), "Error reading video file or webcam"

        # รับคุณสมบัติวิดีโอ: ความกว้าง, ความสูง, และเฟรมต่อวินาที (fps)
        self.w, self.h, self.fps = (int(self.cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

        # กำหนดจุดสำหรับเส้นหรือพื้นที่สนใจในเฟรมวิดีโอ (ค่าเริ่มต้น)
        if line_points is None:
            self.line_points = [(20, int(self.h / 2)), (self.w - 20, int(self.h / 2))]
        else:
            self.line_points = line_points

        # ระบุคลาสที่จะนับ (ค่าเริ่มต้น)
        if classes_to_count is None:
            self.classes_to_count = [0]  # ค่าเริ่มต้นสำหรับ class ID 0 (เช่น คน)
        else:
            self.classes_to_count = classes_to_count

        # ตั้งค่าวิดีโอไรเตอร์เพื่อบันทึกวิดีโอผลลัพธ์
        self.video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (self.w, self.h))

        # ตั้งค่า Object Counter พร้อมตัวเลือกการแสดงผลและพารามิเตอร์อื่นๆ
        self.counter = solutions.ObjectCounter(
            view_img=display_video,  # แสดงภาพระหว่างประมวลผล
            reg_pts=self.line_points,  # จุดพื้นที่สนใจ
            classes_names=self.model.names,  # ชื่อคลาสจากโมเดล YOLO
            draw_tracks=True,  # วาดเส้นติดตามวัตถุ
            line_thickness=2,  # ความหนาของเส้นที่วาด
        )

    def draw_bounding_boxes(self, frame, results):
        for result in results:
            boxes = result.boxes
            for box in boxes:
                xyxy = box.xyxy[0].cpu().numpy()  # ค่าพิกัดกล่องกรอบ
                class_id = int(box.cls[0])  # ID คลาส
                label = f"{self.model.names[class_id]}"  # ป้ายกำกับ

                # วาดกล่องกรอบ
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                # วาดป้ายกำกับ
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame

    def process_video(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            # ดำเนินการติดตามวัตถุในเฟรมปัจจุบัน โดยกรองด้วยคลาสที่ระบุ
            results = self.model(frame, classes=self.classes_to_count)

            # ใช้ Object Counter เพื่อนับวัตถุในเฟรมและรับภาพที่ถูกทำเครื่องหมาย
            annotated_frame = self.counter.start_counting(frame, results)

            # วาดกล่องกรอบบนเฟรมที่ทำเครื่องหมาย
            annotated_frame = self.draw_bounding_boxes(annotated_frame, results)

            # เขียนเฟรมที่ทำเครื่องหมายลงในวิดีโอผลลัพธ์
            self.video_writer.write(annotated_frame)

            # แสดงเฟรมที่ประมวลผลแล้ว
            if self.counter.view_img:
                cv2.imshow('Annotated Frame', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        # ปล่อยวิดีโอแคปเจอร์และวิดีโอไรเตอร์
        self.cap.release()
        self.video_writer.release()

        # ปิดหน้าต่าง OpenCV ทั้งหมด
        cv2.destroyAllWindows()

# ตัวอย่างการใช้งาน:
if __name__ == "__main__":
    use_webcam = True  # ตั้งค่านี้เป็น True เพื่อใช้กล้องเว็บแคม
    video_path = "D:/Machine Learning/object_counting/test.mp4"  # ไฟล์วิดีโอ
    output_path = "object_counting_output.avi"
    yolo_model_path = "yolov8n.pt"
    line_points = [(0, 250), (640, 250)]
    classes_to_count = [0]  # Class IDs for Baby Shrimp

    counter = ObjectCounter(video_path, output_path, yolo_model_path, line_points, classes_to_count, use_webcam=use_webcam)
    counter.process_video()
