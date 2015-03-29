import camera
import sensor
import time
import config

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
    dist = config.DIST_CAMERA_PINS #meters to the pins
    return dist/ball_speed_ms

def init():
    sensor.init()
    camera.init()

def main():

    init()

    while True:
        print "ready for some balls"
        
        #get the speed of the ball
        ms = sensor.wait_sensors()
        
        #calc the time to start capturing the ball impact
        print "taking a series of pictures"
        time_to_impact = calc_ball_impact_time(ms)
        if time_to_impact > config.CAPTURE_IMPACT_DURATION:
            time.sleep(time_to_impact - config.CAPTURE_IMPACT_DURATION)
        
        #capture a series of images  of the impact
        camera.capture_image_sequence_time(config.CAPTURE_IMPACT_DURATION)

        #capture a photo after impact config.CAPTURE_AFTER_IMPACT_TIMEOUT seconds after
        print "capture a photo"
        camera.capture_image(config.CAPTURE_AFTER_IMPACT_TIMEOUT)


if __name__ == "__main__":
    main()
