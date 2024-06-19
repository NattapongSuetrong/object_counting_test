# import RPi.GPIO as GPIO
import time
from detectionV3 import ObjectCounter


PUMP_PIN = 18

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(PUMP_PIN, GPIO.OUT)

def Start():
    print('Start')
    # GPIO.output(PUMP_PIN, GPIO.HIGH)  # เปิดปั๊มน้ำ
    time.sleep(3)
    print('OK')

def Stop():
    # GPIO.output(PUMP_PIN, GPIO.LOW)  # ปิดปั๊มน้ำ
    print('Stop')
    
if __name__ == "__main__":
    video_path = 0  # ถ้าใช้กล้องเว็บแคมเป็น input
    output_path = "object_counting_output.avi"
    Start()
    model_count = ObjectCounter(video_path, output_path)
    model_count.process_video()