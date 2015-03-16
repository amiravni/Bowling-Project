import camera
import sensor

dist = 4.0 #meters to the pins

def main():


    while True:
        ms = sensor.wait_sensors()
	print "taking a video"	
	time_to_record = 1 if dist/ms < 1.0 else dist/ms
        camera.capture_video_time(dist/ms)
        print "capture a photo"
	camera.capture_image()
        
if __name__ == "__main__":
    main()
