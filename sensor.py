import RPi.GPIO as GPIO  
import time
import traceback,sys
import config

t0 = 0.0 #milis
t1 = 0.0 #milis


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.RPI_GPIO_SENSOR1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(config.RPI_GPIO_SENSOR2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def ball_speed_kmh(t0,t1):
    return 3.6*((config.SENSOR_DIST)/((t1-t0)/1000.0))

def ball_speed_ms(t0,t1):
    return ((config.SENSOR_DIST)/((t1-t0)/1000.0))
    
def interupt_sensor1():
    global t0  
    #print "interupt sensor 1"
    t0 =  time.time() * 1000

def interupt_sensor2():
    global t1
    #print "interupt sensor 2" 
    t1 = (time.time() * 1000)

def wait_sensors():

        try:  
            init()
            GPIO.wait_for_edge(config.RPI_GPIO_SENSOR1_PIN, GPIO.FALLING)  
            interupt_sensor1()
            GPIO.wait_for_edge(config.RPI_GPIO_SENSOR2_PIN, GPIO.FALLING)  
            interupt_sensor2()
            print t0,t1
            
            print  ball_speed_kmh(t0,t1)
            GPIO.cleanup()
            return ball_speed_ms(t0,t1)
        except:  
            print "something happend..."  
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60

        GPIO.cleanup()           # clean up GPIO on normal exit 
