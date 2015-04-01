import time

import config
import pin_control_comm
import calculate_pins
import thread
import random
import protocol

if not config.DEBUG:
    import camera
    import sensor
    
import cv2

goOn = True

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


def play_game():
    global goOn
    if config.DEBUG:
        while goOn:
            #impact_image = cv2.imread(create_photo_path(photos_folder,10,19))
            #pin_count = calculate_pins.calculate_pin_count(impact_image)
            pin_control_comm.send_pin_count(random.randint(0,10),random.uniform(0,40))
            time.sleep(1)
    else:

        while goOn:
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
            camera.capture_image_by_time('after_impact',config.CAPTURE_AFTER_IMPACT_TIMEOUT)
            #impact_image = cv2.imread('after_impact.jpg')
            pin_count = calculate_pins.calculate_pin_count('after_impact.jpg')
            pin_control_comm.send_pin_count(pin_count,kmh)
    
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
    global goOn
    init()
    
    while True:
        if pin_control_comm.cmd_sock_is_ready():
            cmd_msg  = pin_control_comm.recv_cmd_sock()
            print 'cmd is : %s' % cmd_msg
            if cmd_msg == protocol.START_CALIB_CMD:
                print 'Got start calib, sending image to base'
                if config.DEBUG:
                    base_image = cv2.imread('base_image.jpg')
                    cv2.imwrite('base_image_comp.jpg',base_image,[int(cv2.IMWRITE_JPEG_QUALITY), 50])
                    base_image_comp = open('base_image_comp.jpg','rb').read()
                    print len(base_image_comp)
                    pin_control_comm.send_jpeg_image(base_image_comp)
                else:
                    camera.capture_image('base_image')
                    base_image = cv2.imread('base_image.jpg')

                    cv2.imwrite('base_image_comp.jpg',base_image,[int(cv2.IMWRITE_JPEG_QUALITY), 70])
                    base_image_comp = open('base_image_comp.jpg','rb').read()
                    
                    pin_control_comm.send_jpeg_image(base_image_comp)
            elif cmd_msg == protocol.START_GAME_CMD:
                print 'Starting the game'
                goOn = True
                #pin_control_comm.send_pin_count(random.randint(0,10),random.uniform(0,40))
                thread.start_new_thread(play_game, ())
            elif cmd_msg == protocol.STOP_GAME_CMD:
                print 'Stoping the game'
                goOn = False
            elif cmd_msg.startswith(protocol.CALIB_RESULT_CMD):
                if len(cmd_msg) > (len(protocol.CALIB_RESULT_CMD) + 1):
                    result = cmd_msg[len(protocol.CALIB_RESULT_CMD)+1:]
                    print "The calib result is : %s" % eval(result)
                    rects = eval(result)
                    fd = open(config.PINS_BBOX_FILE_PATH,'w')
                    for rect in rects:
                        print >> fd, rect
                    fd.close()
                    
                    calculate_pins.init()
                else:
                    print 'Problem getting the calib result'

        time.sleep(0.01)
    


            
            
if __name__ == "__main__":
    main()
