#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 


import RPi.GPIO as GPIO  #for GPIO
import time

GPIO.setmode(GPIO.BCM)
print "++++++++++++++++++++++++"
print "+ Welcome to your home +"
print "++++++++++++++++++++++++"
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT) # for LED
GPIO.setup(25,GPIO.OUT) # for LED
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for shutdown
shutdownSwitch = 10

def shutdown(pin):
	print "shutdown"
	#os.system("sudo shutdown -h now")
	time.sleep(2)

GPIO.add_event_detect(shutdownSwitch, GPIO.FALLING, callback=shutdown,bouncetime=500)



while True:
	print "Salutti"
	time.sleep(1)
