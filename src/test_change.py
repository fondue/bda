#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015

import pickle
import RPi.GPIO as GPIO
import os
import time

# for Change
openOldKitchen = False
closedOldKitchen = True
openedKitchen = False
closedKitchen = True
hasChangedKitchen = False
#global actual_time_kitchen
actual_time_kitchen = time.time()
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
            
def writeOpenKitchen():
    with open('/home/pi/projects/bda/data/time_open_kitchen.pkl','wb') as f:
		value = time.time()
		print value
		pickle.dump(value,f)
		
def writeClosedKitchen():
    with open('/home/pi/projects/bda/data/time_closed_kitchen.pkl','wb') as f:
		value = time.time()
		print value
		pickle.dump(value,f)




def getHasChangedKitchen():
	
	time_open = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
	time_closed = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
	global openOldKitchen
	global closedOldKitchen
	global openedKitchen
	global closedKitchen
	global hasChangedKitchen

	if time_open >= time_closed:
		openedKitchen = True
		closedKitchen = False

	if time_closed >= time_open:
		openedKitchen = False
		closedKitchen = True

	if openOldKitchen == openedKitchen:
		hasChangedKitchen = False
	else:
		hasChangedKitchen = True

	if closedOldKitchen == closedKitchen:
		hasChangedKitchen = False
	else:
		hasChangedKitchen = True
		
	openOldKitchen = openedKitchen
	closedOldKitchen = closedKitchen
	
	return hasChangedKitchen

# Simulates an activity at the beginning of the programm
writeOpenKitchen()
writeClosedKitchen()
actual_time_kitchen = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
# ------------------------------------------------------

while True:
	
	getHasChangedKitchen()
	#global actual_time
	if hasChangedKitchen == True:
		#save timestamp of changed 
		if closedKitchen == True:
			actual_time_kitchen = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
		if openedKitchen == True:
			actual_time_kitchen = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
		
		
	print "-------------"
	print actual_time_kitchen
	
			
	if time.time() - actual_time_kitchen >= 15:
		print "Warnung!"
		actual_time_kitchen = time.time()
		print "Sende mail"
		#sendemail(mailSendFrom, mailSendTo, 'Warnung!', 'Test: Zu wenig Aktivitaet wurde festgestellt!\nGruesse vom PI')

	
	print "actual time kitchen: " + str(actual_time_kitchen)
	print "--------------"
	time.sleep(1)
			
			
			
			
			
			
			
			
