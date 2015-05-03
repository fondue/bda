#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015


import os #for os.system
import time
import RPi.GPIO as GPIO  #for GPIO


GPIO.setmode(GPIO.BCM)
print "hello"
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # wegen Taster
switch = 24


def shutdown(pin):
	os.system("sudo shutdown -h now")
	time.sleep(5)
	

GPIO.add_event_detect(switch, GPIO.RISING, callback=shutdown)


while True:
	print "Eingang aktiv"
	time.sleep(3)
