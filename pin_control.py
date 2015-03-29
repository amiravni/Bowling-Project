import time

import config
import pin_control_comm
import calculate_pins

if not config.DEBUG:
    import camera
    import sensor
import cv2

    
def check_for_foul():
    pass
    
def calc_ball_speed():
    pass
    
def take_picture_of_impact():
    pass
    
def take_picture_after_impact():
    pass
    
def send_pin_count():
    pass


def calc_ball_impact_time(ball_speed_ms):
    if ball_speed_ms is not None:
        dist = config.DIST_CAMERA_PINS #meters to the pins
        return dist/ball_speed_ms
    return 0
   

def init():
    pin_control_comm.init()
    calculate_pins.init()
    if not config.DEBUG:
        sensor.init()
        camera.init()
    
photos_folder = '../bowling/'
scene_id = 10
image_scheme = "images%03d.jpg"

def create_photo_path(folder,scene,id):
    print folder + str(scene) + '/' + image_scheme % id
    return  folder + str(scene) + '/' + image_scheme % id
    
    
    
def main():
    
    init()
    
    if config.DEBUG:
        speed = 24 #kmh
        impact_image = cv2.imread(create_photo_path(photos_folder,10,19))
        pin_count = calculate_pins.calculate_pin_count(impact_image)
        pin_control_comm.send_pin_count(pin_count,speed)
    else:

        while True:
            print "ready for some balls"
            
            #get the speed of the ball
            ms,kmh = sensor.wait_sensors()

            #calc the time to start capturing the ball impact
            print "taking a series of pictures"
            time_to_impact = calc_ball_impact_time(ms)
            if time_to_impact > config.CAPTURE_IMPACT_DURATION:
                time.sleep(time_to_impact - config.CAPTURE_IMPACT_DURATION)
            
            #capture a series of images  of the impact
            camera.capture_image_sequence_time(config.CAPTURE_IMPACT_DURATION)

            #capture a photo after impact config.CAPTURE_AFTER_IMPACT_TIMEOUT seconds after
            print "capture a photo"
            camera.capture_image_by_time(config.CAPTURE_AFTER_IMPACT_TIMEOUT)
            impact_image = cv2.imread("after_impact.jpg")
            pin_count = calculate_pins.calculate_pin_count(impact_image)
            pin_control_comm.send_pin_count(pin_count,kmh)

            
            
if __name__ == "__main__":
    main()
