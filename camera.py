import picamera
import time
import io 

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.shutter_speed=10000

camera.start_preview()

#my_stream = io.BytesIO()

def capture_image():
    print time.time()

    camera.capture_sequence(([ '%f.jpg' % time.time()] ), use_video_port=True)
#    camera.capture('/run/shm/%f.jpg'%time.time())
#    camera.capture(my_stream,'jpeg')
    print time.time()

def capture_image_by_time(time_sec):
    t0 = time.time()
    while time.time() - t0 < time_sec:
        time.sleep(0.0001)
    capture_image()

def capture_video_time(time_sec):
    print 'capturing for %f time' % time_sec

#    camera.resolution = (640, 480)
#    camera.start_recording(my_stream, format='h264', quality=50)
#    camera.wait_recording(1)
#    camera.stop_recording()

#    camera.start_recording('%f.h264' % time.time())
#    time.sleep(time_sec)
#    camera.stop_recording()
    frames = int(20*time_sec)
    camera.capture_sequence(( 'images%03d.jpg' % i for i in range(frames) ), use_video_port=True)
