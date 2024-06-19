import cv2
from ultralytics import YOLO
from ultralytics.solutions import object_counter

class ObjectCounter:
    def __init__(self, video_path, output_path):
        self.model = YOLO("yolov8n.pt")
        self.cap = cv2.VideoCapture(video_path)
        assert self.cap.isOpened(), "Error reading video file"
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.w, self.h = (int(self.cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        print(self.fps)
        self.line_points = [(0, 230), (640, 230)]
        self.classes_to_count = [67]
        self.video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), self.fps, (self.w, self.h))
        self.counter = object_counter.ObjectCounter(
        view_img=True,
        reg_pts=self.line_points,
        classes_names=self.model.names,
        draw_tracks=True,
        line_thickness=1,
        )
        
    def process_video(self):
        while self.cap.isOpened():
            success, im0 = self.cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break

            tracks = self.model.track(im0, persist=True, show=False, classes=self.classes_to_count)
            im0 = self.counter.start_counting(im0, tracks)
            self.video_writer.write(im0)
            
            print(self.counter.in_counts)
            if self.counter.in_counts == 2:
                break

        self.cap.release()
        self.video_writer.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    video_path = 0 # ถ้าใช้กล้องเว็บแคมเป็น input
    output_path = "object_counting_output.avi"
    
    counter = ObjectCounter(video_path, output_path)
    counter.process_video()