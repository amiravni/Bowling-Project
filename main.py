import camera
import sensor
import time

dist = 2.0 #meters to the pins

def main():


    while True:
	print "ready for some balls"
        ms = sensor.wait_sensors()
#	ms = 4
	print "taking a video"	
	time_to_record = 1 if dist/ms < 1.0 else dist/ms
        camera.capture_video_time(time_to_record)
        print "capture a photo"
	camera.capture_image()
	time.sleep(0.01)        
if __name__ == "__main__":
    main()
