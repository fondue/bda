#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 

import RPi.GPIO as GPIO  #for GPIO
import time
import os
import pickle

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


def writeLog():
	with open("/home/pi/projects/bda/data/dauertest_log.txt","a") as f:
		localtime = time.asctime( time.localtime(time.time()) )
		print "Local current time :", localtime
		f.write(str(localtime)+"\n")
		f.close()
		

def writeLastTime():
    with open('/home/pi/projects/bda/data/last_time.pkl','wb') as f:
		value = time.time()
		print value
		pickle.dump(value,f)	

toleranzSchwelle = 8 # 4 Stunden

while True:
	print "Dauertest gestartet"
	for i in range (1,2):
		GPIO.output(24,GPIO.HIGH)
		time.sleep(1)
		GPIO.output(24,GPIO.LOW)
		time.sleep(3)
	lastTime = os.path.getmtime('/home/pi/projects/bda/data/last_time.pkl')
	if time.time() - lastTime >= toleranzSchwelle:
		writeLog()
		print "Zeit notiert"
		writeLastTime()
		print "Warnung versendet"
		#sendemail(mailSendFrom, mailSendTo, 'Warnung!', 'Test: Zu wenig Aktivitaet wurde festgestellt!\nGruesse vom PI')
