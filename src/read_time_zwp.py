#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015


import os #for os.system
import time
import RPi.GPIO as GPIO  #for GPIO
import pickle
import os.path

lastTime=None


GPIO.setmode(GPIO.BCM)
print "hello"
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT)
#GPIO.setup(24,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)  # wegen Taster

maxDiff = 5


#def led():
#	GPIO.output(24,GPIO.LOW)
#	time.sleep(2)
#	GPIO.output(24,GPIO.HIGH)
	
def readLastTime():
	with open('/home/pi/projects/bda/data/last_time.pkl', 'rb') as f:
		t = pickle.load(f)
		print(t)
		return t
		
		#while True:
		#	line = f.readline()
			# Zero length indicates EOF
		#	if len(line) == 0:
				#break
			# The `line` already has a newline
			# at the end of each line
			# since it is reading from a file.
		#	print line
		#	return float(line)
		# close the file
		#f.close()

def writeLastTime():
    with open('/home/pi/projects/bda/data/last_time.pkl','wb') as f:
		value = time.time()
		#print value
		pickle.dump(value,f)
		#lastTime = os.path.getmtime('/home/pi/projects/bda/data/time_zwp.pkl')
		#f.write(str(value))
		#f.close()


	
while True:
	# check: is file existing
    if os.path.isfile('/home/pi/projects/bda/data/last_time.pkl'):
		# time stamp of file (time when last edited)
		lastTime = os.path.getmtime('/home/pi/projects/bda/data/last_time.pkl')
		print lastTime
		if time.time() - lastTime >= maxDiff:
			print "LED ein!"
			GPIO.output(24,GPIO.HIGH)
			time.sleep(1)
			GPIO.output(24,GPIO.LOW)
			writeLastTime()
    time.sleep(1) 



