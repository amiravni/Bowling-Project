import cv2
import config
import os.path


def is_bbox_initialized():
    global pins_bbox
    
    return len(pins_bbox) > 0
    
def get_pins_bbox():
    
    if not os.path.isfile(config.PINS_BBOX_FILE_PATH):
        print 'Error you need to calibrate your camera'
        return None
        
    ret = []
    fd = open(config.PINS_BBOX_FILE_PATH,'r')
    for line in fd.readlines():
        ret.append(eval(line))
    if config.DEBUG:
        print 'Pins bbox is : ',ret

    return ret


pins_bbox = []
pin_rgb_sum_count_epsilon = 0.1
    
def init():
    global pins_bbox
    pins_bbox = get_pins_bbox()

def check_calibration(base_image_path):
    global pins_bbox
    global pin_rgb_sum_count_epsilon
    
    if not os.path.isfile(base_image_path):
        print "Error %s not found can't check the pin count!" % base_image_path
        return
    
    base_image = cv2.imread(base_image_path)
    
    if base_image is None:
        print 'Error loading image %s' % base_image_path
        return
    
    pins = 0
    

    sceneCopy = base_image.copy()

	
    for pin_bbox in pins_bbox:
        
        pin_rect = base_image[pin_bbox[1]:pin_bbox[1]+pin_bbox[3],pin_bbox[0]:pin_bbox[0]+pin_bbox[2]]
        calc_pixels = 0
        for x in pin_rect:
            for y in x:
                calc_pixels += sum(y)
        full_box = (pin_bbox[3]*pin_bbox[2]*255.0*3.0)
        print calc_pixels/full_box
        if calc_pixels/full_box > pin_rgb_sum_count_epsilon:
			
            pins += 1

            cv2.rectangle(sceneCopy,(pin_bbox[0],pin_bbox[1]),(pin_bbox[0]+pin_bbox[2],pin_bbox[1]+pin_bbox[3]),(0,255,0),1)
            cv2.imshow('base',sceneCopy)

    print 'there are %d pins' % pins
    cv2.waitKey(0)
        
def calculate_pin_count(impact_image_path):
    global pins_bbox
    global pin_rgb_sum_count_epsilon
 
 
    if not os.path.isfile(impact_image_path):
        print "Error %s not found can't check the pin count!"
        return
     
    impact_image = cv2.imread(impact_image_path)
     
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
        full_box = (pin_bbox[3]*pin_bbox[2]*255.0*3.0)
        print calc_pixels/full_box
 
        if calc_pixels/full_box > pin_rgb_sum_count_epsilon:
            pins += 1
            if config.DEBUG:
                cv2.rectangle(sceneCopy,(pin_bbox[0],pin_bbox[1]),(pin_bbox[0]+pin_bbox[2],pin_bbox[1]+pin_bbox[3]),(0,255,0),1)
                cv2.imshow('after impact',sceneCopy)
    if config.DEBUG:
        print 'there are %d pins' % pins
        cv2.waitKey(0)
     
    return pins


