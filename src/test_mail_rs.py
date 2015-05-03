#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# Liest ein E-Mail. Falls Code im Subject steht, wird eine Mail zurueck geschickt.

# send
import time, os
#import pickle
import smtplib
# for GPIOs
import RPi.GPIO as GPIO  #for GPIO

# receive
import threading
import picamera, smtplib, sys, time
import email, getpass, imaplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# receive
interval = 3 #check emails every ... sec

MailReceiveUSER = 'muster.bewohner@gmail.com'
MailReceivePWD = 'braunbaer17'
MailReceiveSRV = 'imap.gmail.com'

MailSendUSER = ''
MailSendPWD = ''
MailSendSRV = 'mail.gmx.net'
MailSendFROM = MailReceiveUSER
MailSendTO = 'dominik.imhof@stud.hslu.ch'

# send
mailServer = 'pop.gmail.com'
mailPort = 587
mailLogin = 'muster.bewohner@gmail.com'
mailPass = 'braunbaer17'
mailSendFrom = mailLogin
mailSendTo = 'dominik.imhof@stud.hslu.ch'
mailTLS = True
mailDebug = False

# GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # wegen Taster
switch = 24

def write():
	print 'GPIO Signal erkannt'

GPIO.add_event_detect(switch, GPIO.RISING, callback=write)






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
            
            

running = True

# check Mails
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
                        sendemail(mailSendFrom, mailSendTo, 'Hallo!', 'Kombination der Mail-Systeme erfolgreich!\nGruesse vom PI')
                        for part in mail.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload()
                                #  For each line in message execute instructions
                                with open("/home/pi/projects/bda/data/test.txt","w") as f:
									for line in body.split('\r\n'):
										if line != "":
											print("Wort erkannt")
											f.write(line+"\n")
											#sendMail()
										elif line == "Text":
											print("Text erkannt")
											#...
										#else:
											#print("Nichts erkannt")
                                       
            time.sleep(interval)
    except Exception, e1:
        print("Error...: " + str(e1))
    except (KeyboardInterrupt, SystemExit):
       exit()
            
while True:            
	checkMails()
	time.sleep(4000)
	

