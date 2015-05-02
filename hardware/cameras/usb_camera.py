import time
import io 
import cv2
from threading import Thread, Lock
from thread import start_new_thread


camera = None
current_photo = None
current_photo_lock = Lock()

def init(res,shutter_speed):
    global camera
    exposure_time = 1e9/shutter_speed
    camera = cv2.VideoCapture(0)
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, res[0])
    camera.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, res[1])
    camera.set(cv2.cv.CV_CAP_PROP_EXPOSURE,exposure_time)
    start_new_thread(infinite_capture_photos,())


def infinite_capture_photos():
    global current_photo
    global current_photo_lock
    while True:
        current_photo_lock.acquire()
        try:
            s,current_photo = camera.read()
        finally:
            current_photo_lock.release()
        time.sleep(0.03)

def capture_image(name):
    if camera is None:
        return

    #s, img_rgb = camera.read()
    current_photo_lock.acquire()
    try:
        img_rgb = current_photo 
    finally:
        current_photo_lock.release()
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

