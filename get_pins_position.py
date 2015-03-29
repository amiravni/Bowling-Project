import cv2
import time

photos_folder = '../bowling_pins_photos/'
scene_id = 4 
image_scheme = "images%03d.jpg"

def create_photo_path(folder,scene,id):
    print folder + str(scene_id) + '/' + image_scheme % id
    return folder + str(scene_id) + '/' + image_scheme % id

rectangle = False
recv_over = True
rect = []
ix = 0
iy = 0

rects = []

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

        cv2.imshow('image', sceneCopy)

    
    

image = cv2.imread(create_photo_path(photos_folder,scene_id,0))
print create_photo_path(photos_folder,scene_id,0)
cv2.namedWindow('image')
cv2.setMouseCallback('image',onmouse)
scale = 4
window_width = int(image.shape[1]*scale)
window_height = int(image.shape[0]*scale)
cv2.resizeWindow('image', window_width, window_height)
cv2.imshow('image', image)
while 1:
    k = cv2.waitKey(33)
    if k==13: #save rect
        rects.append(rect)
        print rects
    if k==115: #s char
        fd = open('pins_bbox.txt','w')
        for rect in rects:
            print >> fd, rect
        fd.close()
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print k # else print its value
