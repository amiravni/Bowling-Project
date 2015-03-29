import cv2

pins_bbox_file = 'pins_bbox.txt'
pins_bbox = []

photos_folder = './bowling_pins_photos/'
scene_id = 4 
image_scheme = "images%03d.jpg"

pin_pixel_epsilon = 4000

def create_photo_path(folder,scene,id):
    print folder + str(scene) + '/' + image_scheme % id
    return  folder + str(scene) + '/' + image_scheme % id

def get_pins_bbox():
    ret = []
    fd = open(pins_bbox_file,'r')
    for line in fd.readlines():
        ret.append(eval(line))
    print 'Pins bbox is : ',ret
    return ret


def get_pixels_rgb_count(matrix):
    calc_pixels = 0
    for x in matrix:
        for y in x:
            calc_pixels += sum(y)
    return calc_pixels

    
pins_bbox = get_pins_bbox()

base_image = cv2.imread(create_photo_path(photos_folder,17,0))
impact_image = cv2.imread(create_photo_path(photos_folder,17,19))
sceneCopy = impact_image.copy()

pins = 0
for pin_bbox in pins_bbox:
    #print pin_bbox
    
    before_pin_pixels = base_image[pin_bbox[1]:pin_bbox[1]+pin_bbox[3],pin_bbox[0]:pin_bbox[0]+pin_bbox[2]]
    after_pin_pixels = impact_image[pin_bbox[1]:pin_bbox[1]+pin_bbox[3],pin_bbox[0]:pin_bbox[0]+pin_bbox[2]]
    
    print get_pixels_rgb_count(before_pin_pixels) - get_pixels_rgb_count(after_pin_pixels)
    if (get_pixels_rgb_count(before_pin_pixels) - get_pixels_rgb_count(after_pin_pixels)) > pin_pixel_epsilon:
        pins += 1
    else:
        cv2.rectangle(sceneCopy,(pin_bbox[0],pin_bbox[1]),(pin_bbox[0]+pin_bbox[2],pin_bbox[1]+pin_bbox[3]),(0,255,0),1)
        cv2.imshow('image',sceneCopy)

        
print 'there are %d pins' % pins
#cv2.imshow('after impact',impact_image)
cv2.waitKey(0)