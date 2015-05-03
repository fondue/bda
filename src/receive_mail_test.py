#!/usr/bin/python
import threading
import picamera, smtplib, sys, time
import email, getpass, imaplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

interval = 3 #check emails every ... sec

MailReceiveUSER = 'muster.bewohner@gmail.com'
MailReceivePWD = 'braunbaer17'
MailReceiveSRV = 'imap.gmail.com'

MailSendUSER = ''
MailSendPWD = ''
MailSendSRV = 'mail.gmx.net'
MailSendFROM = MailReceiveUSER
MailSendTO = 'dominik.imhof@stud.hslu.ch'


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


# Send EMail
#def sendMail( msg='Ihre Anfrage', subject='Antwort vom Pi', raspicam=False ):
#    if raspicam:
        # Foto erstellen
#        fn = 'foto.jpg'
#        camera = picamera.PiCamera()
#        camera.capture(fn, resize=(640,480))
#        camera.close()
    # E-Mail zusammensetzen
#    mime = MIMEMultipart()
#    mime['From'] = MailSendFROM
#    mime['To'] = MailSendTO
#    mime['Subject'] = Header(subject, 'utf-8')
#    mime.attach(MIMEText(msg, 'plain', 'utf-8'))
    # Bild hinzufuegen
#    if raspicam:
#        f = open(fn, 'rb')
#        img = MIMEImage( f.read() )
#        f.close()
#        mime.attach(img)
    # Mail versenden
    
#def sendMail():
#    smtp = smtplib.SMTP(MailSendSRV)
#    smtp.starttls()
#    smtp.login(MailSendUSER, MailSendPWD)
#    smtp.sendmail(MailSendFROM, [MailSendTO], "Hello")
#   smtp.quit()


checkMails()


#if __name__ == '__main__':
#    try:
#        running = True
#        # Start checkMails Thread
#        checkMails_thread = threading.Thread(target=checkMails)
#        checkMails_thread.start()
#    except Exception, e1:
#        print("Error...: " + str(e1))
#    except (KeyboardInterrupt, SystemExit):
#        running = False
#        print("Schliesse Programm..")

# this is the main (2.) thread which exits after all is done, so Dont close here! 
