#!/usr/bin/python

import time
import picamera
import glob, os

frames = 1
xres = 2592
yres = 1944
j = 1

while (xres > 20):
  with picamera.PiCamera() as camera:
    jexp = '/run/shm/*.jpg'  # first, clear out the jpegs in this directory
    plist = glob.glob(jexp)
    for fname in plist:
      os.remove(fname)
    camera.resolution = (xres, yres)
    camera.start_preview()
    time.sleep(2)  # wait for autoexposure to work
    print 'start capture'
    start = time.time()
    camera.capture_sequence(( '/run/shm/image%03d.jpg' % i for i in range(frames) ), use_video_port=True)
    print('%d  %dx%d: Captured %d images at %.2ffps' % (j, xres, yres, frames, (frames / (time.time() - start))))
    camera.stop_preview()
    xres = xres / 2
    yres = yres / 2
    frames = 60
    j = j + 1
    exit()

