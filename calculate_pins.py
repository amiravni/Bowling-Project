import cv2
import config
import os.path



def get_pins_bbox():
    
    if not os.path.isfile(config.PINS_BBOX_FILE_PATH):
        print 'Error you need to calibrate your camera'
        exit(-1)
        
    ret = []
    fd = open(config.PINS_BBOX_FILE_PATH,'r')
    for line in fd.readlines():
        ret.append(eval(line))
    if config.DEBUG:
        print 'Pins bbox is : ',ret

    return ret


pins_bbox = []
pin_rgb_sum_count_epsilon = 40000
    
def init():
    global pins_bbox
    pins_bbox = get_pins_bbox()

def calculate_pin_count(impact_image):
    global pins_bbox
    global pin_rgb_sum_count_epsilon
    
    if impact_image is None:
        return config.FULL_PIN_COUNT
    
    pins = 0
    
    if config.DEBUG:
        sceneCopy = impact_image.copy()
    
    for pin_bbox in pins_bbox:
        
        pin_rect = impact_image[pin_bbox[1]:pin_bbox[1]+pin_bbox[3],pin_bbox[0]:pin_bbox[0]+pin_bbox[2]]
        calc_pixels = 0
        for x in pin_rect:
            for y in x:
                calc_pixels += sum(y)
        
        if calc_pixels > pin_rgb_sum_count_epsilon:
            pins += 1
            if config.DEBUG:
                cv2.rectangle(sceneCopy,(pin_bbox[0],pin_bbox[1]),(pin_bbox[0]+pin_bbox[2],pin_bbox[1]+pin_bbox[3]),(0,255,0),1)
                cv2.imshow('image',sceneCopy)
    if config.DEBUG:
        print 'there are %d pins' % pins
        #cv2.imshow('after impact',impact_image)
        cv2.waitKey(0)
    
    return pins


