import RPi.GPIO as GPIO  
import time
import traceback,sys
  
t0 = 0.0 #milis
t1 = 0.0 #milis
sensor_dist = 0.3 #meters

def interupt_sensor1():
    global t0  
    #print "interupt sensor 1"
    t0 =  time.time() * 1000


def interupt_sensor2():
    global t1
    #print "interupt sensor 2" 
    t1 = (time.time() * 1000)

def wait_sensors():

        GPIO.setmode(GPIO.BCM)  
  
        # GPIO 23 set up as input. It is pulled down to receive the signal form arduino  
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
  
#        print "Waiting for falling edge on port 23"  
          
        # raspi is now not looking for falling but rising edge. so if the digital pin on arduino goes high it triggers the raspi  
        try:  
            GPIO.wait_for_edge(25, GPIO.FALLING)  
#            print "\nRising edge detected."  
            interupt_sensor1()
            GPIO.wait_for_edge(23, GPIO.FALLING)  
            interupt_sensor2()
#            print t1-t0
            print  3.6*((sensor_dist)/((t1-t0)/1000.0))
            GPIO.cleanup()
            return (sensor_dist)/((t1-t0)/1000.0)
	    
        except:  
            print "something happend..."  
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60

        GPIO.cleanup()           # clean up GPIO on normal exit 
        
#        return None
