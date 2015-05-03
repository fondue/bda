#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015


import os #for os.system
import time
import RPi.GPIO as GPIO  #for GPIO


GPIO.setmode(GPIO.BCM)
print "hello"
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.OUT)
#GPIO.setup(24,GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)  # wegen Taster

maxDiff = 10


#def led():
#	GPIO.output(24,GPIO.LOW)
#	time.sleep(2)
#	GPIO.output(24,GPIO.HIGH)
	
def readLastTime():
	with open('/home/pi/projects/bda/data/enocean_time.txt') as f:
		while True:
			line = f.readline()
			# Zero length indicates EOF
			if len(line) == 0:
				break
			# The `line` already has a newline
			# at the end of each line
			# since it is reading from a file.
			print line
			return float(line)
		# close the file
		f.close()

def writeLastTime():
    with open('/home/pi/projects/bda/data/enocean_time.txt','w') as f:
		value = time.time()
		f.write(str(value))
		f.close()
		
if time.time() - readLastTime() >= maxDiff:
	print "LED ein!"
	GPIO.output(24,GPIO.HIGH)
	time.sleep(2)
	GPIO.output(24,GPIO.LOW)
	writeLastTime()

#led



