# v0.1 by Dominik Imhof 03.2015

import pickle
import time, os #for crontab
import RPi.GPIO as GPIO  #for GPIO


GPIO.setmode(GPIO.BCM)
print "hello"
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # wegen Taster
GPIO.setup(22,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # wegen Taster
sensor1 = 17
sensor2 = 22


def writeLastTime(pin):
	test = time.time()
	print time.time()
	file = open("/home/pi/projects/dtrace/data/time_file_gpio.pkl","wb")
	pickle.dump(test,file)
	file.close()


GPIO.add_event_detect(sensor1, GPIO.RISING, callback=writeLastTime)
GPIO.add_event_detect(sensor2, GPIO.RISING, callback=writeLastTime)


while True:
	print "Eingang aktiv"
	time.sleep(1)
	
	



# print time.time()

#timeFile = "/tmp/lasttimestamp"
#maxDiff = 90 #in sekunden

#def getLastTime():
#  with open(timeFile, 'r') as file:
#    timestamp = file.readline()
#  return timestamp

#def writeLastTime(zeit):
#  with open(timeFile, 'w') as file:  # with open, weil schliesst so automatisch
#    file.write(zeit)

#GPIO.add_event_detect(sensor, GPIO.RISING, callback = writeLastTime)

# nur ausfuehren wenn Bewegung...


#while True:
#	if os.path.isfile(timeFile):
#		lastTime = float(getLastTime())
#		if time.time() - lastTime >= maxDiff:
#			print "Letzter Zugriff ist zu lange her {}".format( time.asctime( time.localtime( lastTime ) ) )
		





