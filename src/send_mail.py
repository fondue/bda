#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 

import time, os
import pickle

import smtplib

mailServer = 'asmtp.mail.hostpoint.ch'
mailPort = 587
mailLogin = 'bda15-inat@ihomelab-lists.ch'
mailPass = 'PCnO5CMU'
mailSendFrom = mailLogin
mailSendTo = 'dominik.imhof@stud.hslu.ch'
#mailSendTo = 'imhof_dominik@hotmail.com'
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

def readSchwelleNachtString():
	f = open('/home/pi/projects/bda/data/schwelle_nacht.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The `line` already has a newline
		# at the end of each line
		# since it is reading from a file.
		#print line
		return line
	# close the file
	f.close()
	
errorSchwelleNacht = True

#def sendError():
	
	#global errorSchwelleNacht
	#if errorSchwelleNacht == True:
	#	errorSchwelleNacht = False
	#	toleranzSchwelleNachtFehler = readSchwelleNachtString()
	#	return "Error: " + toleranzSchwelleNachtFehler 
	
toleranzSchwelleNachtFehler = "Fehler Schwelle Nacht: " + readSchwelleNachtString()


print "sende email" 

if __name__ == '__main__':
	sendemail(mailSendFrom, mailSendTo, "Warnung", toleranzSchwelleNachtFehler)

