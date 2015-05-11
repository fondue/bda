#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 


import RPi.GPIO as GPIO  #for GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT) # for LED
GPIO.setup(25,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for shutdown
GPIO.setup(9,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # switch
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # switch
switch1 = 11
shutdownSwitch = 10
switch = 9

def shutdown(pin):
	print "shutdown"
	#os.system("sudo shutdown -h now")
	time.sleep(1)
	



GPIO.add_event_detect(shutdownSwitch, GPIO.RISING, callback=shutdown)
GPIO.add_event_detect(switch, GPIO.RISING, callback=shutdown)
GPIO.add_event_detect(switch1, GPIO.RISING, callback=shutdown)

while True:
	GPIO.output(24,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(24,GPIO.LOW)

	GPIO.output(25,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(25,GPIO.LOW)

	GPIO.output(7,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(7,GPIO.LOW)

	GPIO.output(8,GPIO.HIGH)
	time.sleep(1)
	GPIO.output(8,GPIO.LOW)
