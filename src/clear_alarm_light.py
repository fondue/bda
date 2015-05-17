#!/usr/bin/python
# v0.1 by Dominik Imhof 05.2015

# GPIO
import RPi.GPIO as GPIO  #for GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.OUT) # for LED absent

GPIO.output(8,GPIO.LOW)
