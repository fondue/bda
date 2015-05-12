#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015

import pickle
import RPi.GPIO as GPIO
import os
import time

# for Change
openOld = False
closedOld = True
opened = False
closed = True
hasChanged = False
global actual_time
actual_time = time.time()
#------------------------


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT) # for LED
GPIO.setup(25,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for shutwodn
shutdownSwitch = 25

def shutdown(pin):
	print "shutdown"
	os.system("sudo shutdown -h now")
	time.sleep(10)	

GPIO.add_event_detect(shutdownSwitch, GPIO.RISING, callback=shutdown)

# Send
import smtplib

# Send Mail
mailServer = 'pop.gmail.com'
mailPort = 587
mailLogin = 'muster.bewohner@gmail.com'
mailPass = 'braunbaer17'
mailSendFrom = mailLogin
mailSendTo = 'dominik.imhof@stud.hslu.ch'
mailTLS = True
mailDebug = False

def sendemail(from_addr, to_addr, subject, message):
    try:
        header = 'From: %s\n' % from_addr
        header+= 'To: %s\n' % to_addr
        header+= 'Subject: %s\n\n' % subject
        message = header + message
        conn = smtplib.SMTP(mailServer, mailPort)
        if mailDebug:
            conn.set_debuglevel(True) #show communication with the server
        if mailTLS:
            conn.starttls()
        conn.login(mailLogin, mailPass)
        error = conn.sendmail(from_addr, to_addr, message)
        if not error:
            print "Successfully sent email"
    except Exception, e:
        print "\nSMTP Error: " + str(e)
    finally:
        if conn:
            conn.quit()

def writeLastTimeOpen():
    with open('/home/pi/projects/bda/data/time_open.pkl','wb') as f:
		value = time.time()
		print value
		pickle.dump(value,f)

def writeLastTimeClosed():
    with open('/home/pi/projects/bda/data/time_closed.pkl','wb') as f:
		value = time.time()
		print value
		pickle.dump(value,f)


def getHasChangedKitchen():
	
	time_open = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
	time_closed = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
	global openOld
	global closedOld
	global opened
	global closed
	global hasChanged

	if time_open >= time_closed:
		opened = True
		closed = False

	if time_closed >= time_open:
		opened = False
		closed = True

	if openOld == opened:
		hasChanged = False
	else:
		hasChanged = True

	if closedOld == closed:
		hasChanged = False
	else:
		hasChanged = True
		
	openOld = opened
	closedOld = closed
	
	return hasChanged



#writeLastTimeOpen()
#time.sleep(1)
#writeLastTimeClosed()

while True:
	
	getHasChangedKitchen()
	#global actual_time
	if hasChanged == True:
		#save timestamp of changed 
		if closed == True:
			actual_time = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
		if opened == True:
			actual_time = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
		
		
	print "-------------"
	print actual_time
	
			
	if time.time() - actual_time >= 15:
		print "Warnung!"
		actual_time = time.time()
		print "Sende mail"
		#sendemail(mailSendFrom, mailSendTo, 'Warnung!', 'Test: Zu wenig Aktivitaet wurde festgestellt!\nGruesse vom PI')

	
	print "actual time: " + str(actual_time)
	print "--------------"
	time.sleep(1)
			
			
			
			
			
			
			
			
