import picamera
import time
import io 
import config

camera = None

def init():
    global camera

    camera = picamera.PiCamera()
    camera.resolution = config.CAMERA_RESOLUTION
    camera.shutter_speed = config.CAMERA_SHUTTER_SPEED
    camera.start_preview()


def capture_image():
    if camera is None:
        return
    print time.time()

    camera.capture_sequence(([ 'after_impact.jpg' ] ), use_video_port=True)
    
    print time.time()

def capture_image_by_time(time_sec):
    if camera is None:
        return
    t0 = time.time()
    while time.time() - t0 < time_sec:
        time.sleep(0.001)
    capture_image()

def capture_image_sequence_time(time_sec):
    global camera
    
    if camera is None:
        return
    print 'capturing for %f time' % time_sec

    frames = int(20*time_sec)
    camera.capture_sequence(( 'images%03d.jpg' % i for i in range(frames) ), use_video_port=True)
