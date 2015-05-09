#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 

import time, os
import pickle
# Send
import smtplib
# GPIO
import RPi.GPIO as GPIO  #for GPIO
# Receive
import threading
import picamera, smtplib, sys, time
import email, getpass, imaplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#------------------------------------------------

# GPIO
GPIO.setmode(GPIO.BCM)
print "hello"
GPIO.setwarnings(False)
# for LED
GPIO.setup(24,GPIO.OUT)
# for Shutwodn
GPIO.setup(25,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
switch = 25

def shutdown(pin):
	print "shutdown"
	#os.system("sudo shutdown -h now")
	time.sleep(10)	

GPIO.add_event_detect(switch, GPIO.RISING, callback=shutdown)



# Receive Mail
interval = 3 #check emails every ... sec

MailReceiveUSER = 'muster.bewohner@gmail.com'
MailReceivePWD = 'braunbaer17'
MailReceiveSRV = 'imap.gmail.com'

MailSendUSER = ''
MailSendPWD = ''
MailSendSRV = 'mail.gmx.net'
MailSendFROM = MailReceiveUSER
MailSendTO = 'dominik.imhof@stud.hslu.ch'

# Send Mail
mailServer = 'pop.gmail.com'
mailPort = 587
mailLogin = 'muster.bewohner@gmail.com'
mailPass = 'braunbaer17'
mailSendFrom = mailLogin
#mailSendTo = 'dominik.imhof@stud.hslu.ch'
mailTLS = True
mailDebug = False
#------------------------------------------------------------------

maxDiff = 20


#-------------------------------------------------------------------

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

# check Mails
running = True

def checkMails():
    try:
        print("read mails")
        m = imaplib.IMAP4_SSL(MailReceiveSRV)
        m.login(MailReceiveUSER, MailReceivePWD)
        if running:
            m.select("Inbox")
            status, unreadcount = m.status('INBOX', "(UNSEEN)")
            unreadcount = int(unreadcount[0].split()[2].strip(').,]'))
            if unreadcount > 0:
                items = m.search(None, "UNSEEN")
                items = str(items[1]).strip('[\']').split(' ')
                for index, emailid in enumerate(items):
                    #print "emailid: " + emailid
                    resp, data = m.fetch(emailid, "(RFC822)")
                    email_body = data[0][1]
                    mail = email.message_from_string(email_body)
                    if mail["Subject"] == 'Code':
                        for part in mail.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload()
                                #  For each line in message execute instructions
								for line in body.split('\r\n'):
									if line != " ":
										if line[0:5] == "mail:":
											address = line[6:len(line)]
											print address
											with open("/home/pi/projects/bda/data/address.txt","w") as f:
												f.write(address+"\n")
												f.close()
												
										if line[0:9] == "schwelle:":
											schwelle = line[10:len(line)]
											print schwelle
											with open("/home/pi/projects/bda/data/schwelle.txt","w") as f:
												f.write(schwelle+"\n")
												f.close()
                                       
            time.sleep(interval)
    except Exception, e1:
        print("Error...: " + str(e1))
    except (KeyboardInterrupt, SystemExit):
       exit()


#def writeLastTime():
#    with open('/home/pi/projects/bda/data/last_time.txt','w') as f:
#		value = time.time()
#		f.write(str(value))
#		f.close()

def readLastTime():
	with open('/home/pi/projects/bda/data/last_time.pkl', 'rb') as f:
		t = pickle.load(f)
		print(t)
		return t
        
def writeLastTime():
    with open('/home/pi/projects/bda/data/last_time.pkl','wb') as f:
		value = time.time()
		#print value
		pickle.dump(value,f)
		#lastTime = os.path.getmtime('/home/pi/projects/bda/data/time_zwp.pkl')
		#f.write(str(value))
		#f.close()
	
def readSchwelle():
	f = open('/home/pi/projects/bda/data/schwelle.txt')
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

def readAddress():
	f = open('/home/pi/projects/bda/data/address.txt')
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
	
while True:
	
	checkMails()
	address = readAddress()
	print address
	schwelle = readSchwelle()
	print schwelle

	
	# check: is file existing
	if os.path.isfile('/home/pi/projects/bda/data/last_time.pkl'):
		# time stamp of file (time when last edited)
		lastTime = os.path.getmtime('/home/pi/projects/bda/data/last_time.pkl')
		print lastTime
		# check Toleranz
		if time.time() - lastTime >= maxDiff:
			print "LED ein!"
			GPIO.output(24,GPIO.HIGH)
			time.sleep(1)
			GPIO.output(24,GPIO.LOW)
			writeLastTime()
			if __name__ == '__main__':
				print "sende Warnung"
				#sendemail(mailSendFrom, address, schwelle, 'Hallo, zu wenig Aktivitaet in der Wohnung vom Muster Bewohner wurde festgestellt!\nGruesse vom PI')
	time.sleep(30) 
		


		
