#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 

import time, os
import pickle

import smtplib

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

maxDiff = 120



def writeLastTime():
    with open("/home/pi/projects/bda/data/time_file.pkl","wb") as f:
        pickle.dump(time.time(),f)

def readLastTime():
    with open("/home/pi/projects/bda/data/time_file.pkl","rb") as f:
        t = pickle.load(f)
        print(t)
        return t
 
 
while True:
	       
	print "last time:"
        
#def writeLastTime():
#	test = time.time()
#	file = open("/home/pi/test_zeit_datei.pkl","wb")
#	pickle.dump(test,file)
#	file.close()


	if time.time() - readLastTime() >= maxDiff:
		print "sende email" 
		writeLastTime()
		if __name__ == '__main__':
			sendemail(mailSendFrom, mailSendTo, 'Alarm!', 'Hallo, zu wenig Aktivitaet in der Wohnung vom Muster Bewohner wurde festgestellt!\nGruesse vom PI')
	time.sleep(60)
		


		
