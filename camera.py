import picamera
import time

camera = picamera.PiCamera()

def capture_image():
    print time.time()
    camera.capture('%f.jpg'%time.time())
    print time.time()

def capture_image_by_time(time_sec):
    t0 = time.time()
    while time.time() - t0 < time_sec:
        time.sleep(0.0001)
    capture_image()

def capture_video_time(time_sec):
   camera.start_recording('video.h264')
   time.sleep(time_sec)
   camera.stop_recording()
