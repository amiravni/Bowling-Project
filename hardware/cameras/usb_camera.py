import time
import io 
import cv2

camera = None

def init(res,shutter_speed):
    global camera
    exposure_time = 1e9/shutter_speed
    camera = cv2.VideoCapture(0)
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, res[0])
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, res[1])
    camera.set(cv2.cv.CV_CAP_PROP_EXPOSURE,exposure_time)


def capture_image(name):
    if camera is None:
        return

    s, img_rgb = camera.read()
    cv2.imwrite(name,img_rgb)


def capture_image_by_time(name,time_sec):
    if camera is None:
        return
    t0 = time.time()
    while time.time() - t0 < time_sec:
        time.sleep(0.001)
    capture_image(name)

def capture_image_sequence_time(time_sec):
    global camera
    
    if camera is None:
        return

    frames = int(20*time_sec)
    for i in range(0,frames):
        capture_image( 'images%03d.jpg'  % i)

