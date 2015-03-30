import cv2
import os.path

import config

rectangle = False
rect_over = True
rects = []
rect = []
ix = 0
iy = 0
image = None

def init_vals():
    global image,rectangle,rect,ix,iy,rect_over, roi,rects
 
    rectangle = False
    rect_over = True
    rects = []
    rect = []
    ix = 0
    iy = 0
    image = None

def onmouse(event,x,y,flags,params):
    global image,rectangle,rect,ix,iy,rect_over, roi

    # Draw Rectangle
    if event == cv2.EVENT_LBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
#            cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)
            rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))

    elif event == cv2.EVENT_LBUTTONUP:
        rectangle = False
        rect_over = True
        print rect
        sceneCopy = image.copy()
        cv2.rectangle(sceneCopy,(ix,iy),(x,y),(0,255,0),1)

        rect = (min(ix,x),min(iy,y),abs(ix-x),abs(iy-y))       
        roi = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        cv2.imshow('calib_window', sceneCopy)

def calib_camera(image_path):
    global rect,rects,image
    
    init_vals()

    if not os.path.isfile(image_path):
        print "Error: %s doesn't exist" % image_path
        return
    
    image = cv2.imread(image_path)
    
    cv2.namedWindow('calib_window')
    cv2.setMouseCallback('calib_window',onmouse)
    
    window_width = int(image.shape[1])
    window_height = int(image.shape[0])
    cv2.resizeWindow('calib_window', window_width, window_height)
    cv2.imshow('calib_window', image)
    
    while 1:
        
        k = cv2.waitKey(33)
        
        if k==13: #save rect
            rects.append(rect)
            print rects

        if k==115: #s char
            fd = open(config.PINS_BBOX_FILE_PATH,'w')
            for rect in rects:
                print >> fd, rect
            fd.close()
            cv2.destroyAllWindows()
            return rects

        if k==27:    # Esc key to stop
            break
        elif k==-1:  # normally -1 returned,so don't print it
            continue
        else:
            print k # else print its value
