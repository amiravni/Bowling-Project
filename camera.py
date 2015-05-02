import config
import time
exec ('import hardware.cameras.%s as camera' % config. CAMERA_NAME)

def init(res,shutter_speed):
    camera.init(res,shutter_speed)


def capture_image(name):
    print time.time()
    camera.capture_image(name)
    print time.time()

def capture_image_by_time(name,time_sec):
    camera.capture_image_by_time(name,time_sec)

def capture_image_sequence_time(time_sec):
    print 'capturing for %f time' % time_sec
    camera.capture_image_sequence_time(time_sec)