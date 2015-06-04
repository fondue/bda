#!/usr/bin/python
# v0.1 by Dominik Imhof 05.2015
# This script will be started automatically after booting the raspberry pi.
# This script implies the logic of the detection of the inactivity.
# This checks the inactivity time and the configuration from the user.
# It sends messages when the barrier is overshoot.

import time, os
import pickle
# Send
import smtplib
# GPIO
import RPi.GPIO as GPIO  #for GPIO
# Receive
import sys
import email, getpass, imaplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#------------------------------------------------

# GPIO
GPIO.setmode(GPIO.BCM)
print "++++++++++++++++++++++++"
print "+ Welcome to your home +"
print "++++++++++++++++++++++++"
GPIO.setwarnings(False)
GPIO.setup(24,GPIO.OUT) # for LED quitt
GPIO.setup(25,GPIO.OUT) # for LED warning
GPIO.setup(8,GPIO.OUT) # for LED alarm
GPIO.output(24,GPIO.LOW)
GPIO.output(25,GPIO.LOW)
GPIO.output(8,GPIO.LOW)
GPIO.setup(10,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for shutdown
shutdownSwitch = 10
GPIO.setup(9,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for quittieren
acknowledge_button = 9
GPIO.setup(11,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # for residentAbsent
residentAbsent = 11

# for change detection
openOldKitchen = False
closedOldKitchen = True
openedKitchen = False
closedKitchen = True
hasChangedKitchen = False
lastTimeEntrance = time.time()

openOldEntrance = False
closedOldEntrance = True
openedEntrance = False
closedEntrance = True
hasChangedEntrance = False
lastTimeEntrance = time.time()

#------------------------

# for errors in Mail Text
errorDayStart = False
errorNightStart = False
errorBarrierNight = False
errorBarrierDay = False
#-----------------------

#Init Configuration-values
addressInit = "bda15-inat@ihomelab-lists.ch"
with open("/home/pi/projects/bda/data/address.txt","w") as f:			
	f.write(addressInit)
	f.close()
with open("/home/pi/projects/bda/data/address_old.txt","w") as f:			
	f.write(addressInit)
	f.close()

barrierDayInitString = "10"
barrierDayInitInt = 10
with open("/home/pi/projects/bda/data/barrier_day.txt","w") as f:			
	f.write(barrierDayInitString)
	f.close()
with open("/home/pi/projects/bda/data/barrier_day_old.txt","w") as f:			
	f.write(barrierDayInitString)
	f.close()	

barrierNightInitString = "15"
barrierNightInitInt = 15
with open("/home/pi/projects/bda/data/barrier_night.txt","w") as f:			
	f.write(barrierNightInitString)
	f.close()
with open("/home/pi/projects/bda/data/barrier_night_old.txt","w") as f:			
	f.write(barrierNightInitString)
	f.close()
	
dayStartInitString = "8"
dayStartInitInt = 8
with open("/home/pi/projects/bda/data/day_start.txt","w") as f:			
	f.write(dayStartInitString)
	f.close()
with open("/home/pi/projects/bda/data/day_start_old.txt","w") as f:			
	f.write(dayStartInitString)
	f.close()

nightStartInitString = "22"
nightStartInitInt = 22
with open("/home/pi/projects/bda/data/night_start.txt","w") as f:			
	f.write(nightStartInitString)
	f.close()
with open("/home/pi/projects/bda/data/night_start_old.txt","w") as f:			
	f.write(nightStartInitString)
	f.close()
#--------------------------------	


# Receive mail

MailReceiveUSER = 'bda15-inat@ihomelab-lists.ch'
MailReceivePWD = 'PCnO5CMU'
# MailReceiveSRV = 'imap.hslu.ch'
MailReceiveSRV = 'imap.mail.hostpoint.ch'

MailSendUSER = ''
MailSendPWD = ''
MailSendSRV = 'mail.gmx.net'
MailSendFROM = MailReceiveUSER


# Send Mail
mailServer = 'asmtp.mail.hostpoint.ch'
mailPort = 587
mailLogin = 'bda15-inat@ihomelab-lists.ch'
mailPass = 'PCnO5CMU'
mailSendFrom = mailLogin
mailTLS = True
mailDebug = False
#------------------------------------------------------------------

warning = False
absent_bool = False #for enabling system when resident comes home
absent_count = False #for only enter the for loop once

# for detection a change of the barriers from night to day
localtime = time.localtime(time.time()).tm_hour
if localtime >= dayStartInitInt and localtime < nightStartInitInt:
	night_old = False
else:
	night_old = True


#-------------------------------------------------------------------

#Interrupts GPIO

# Shutdown switch
def shutdown(pin):
	print "shutdown"
	os.system("sudo shutdown -h now")
	time.sleep(3)	

GPIO.add_event_detect(shutdownSwitch, GPIO.FALLING, callback=shutdown,bouncetime=500)

# Resident absent
def absent(pin):
	print "Absent"
	global absent_bool
	global absent_count
	absent_bool = True # for creating time for the resident to leave the house
	absent_count = True # for creating time for the resident to leave the house
	# For blink LED when absent button is pressed. So the resident is informed that 
	# the system is going to sleep. 
	GPIO.output(8,GPIO.HIGH)
	time.sleep(0.2)
	GPIO.output(8,GPIO.LOW)
	time.sleep(0.2)
	GPIO.output(8,GPIO.HIGH)
	time.sleep(0.2)
	GPIO.output(8,GPIO.LOW)
	time.sleep(0.2)
	GPIO.output(8,GPIO.HIGH)
	time.sleep(0.2)
	GPIO.output(8,GPIO.LOW)
	time.sleep(0.2)
	GPIO.output(8,GPIO.HIGH)
	time.sleep(0.2)
	GPIO.output(8,GPIO.LOW)
	time.sleep(1)

GPIO.add_event_detect(residentAbsent, GPIO.FALLING, callback=absent,bouncetime=1000)
#--------------------------------------------------------------------

# Send Mail
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
newMails = False

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
                    if mail["Subject"] == 'Code': # 'Code' ist the Code-Word that has to be in the subject line
						print "New mail received: Code-Word accepted"
						global newMails 
						newMails = True
						for part in mail.walk():
							if part.get_content_type() == 'text/plain':
								body = part.get_payload()
								# print "got payload"
                                # For each line in message execute instructions
								for line in body.split('=0A=\r\n'):
									if line != " ":
										#print "lese..."
										if line[0:7] == "E-Mail:":
											address = line[8:len(line)]
											print "Adresse aus der Mail gelesen"
											with open("/home/pi/projects/bda/data/address.txt","w") as f:
												f.write(address)
												f.close()
											continue
												
										if line[0:13] == "Schwelle Tag:":
											barrierDay = line[14:len(line)]
											print "Schwelle Tag aus der Mail gelesen"
											with open("/home/pi/projects/bda/data/barrier_day.txt","w") as f:
												f.write(barrierDay)
												#f.close()
											continue
										
										if line[0:15] == "Schwelle Nacht:":
											barrierNight = line[16:len(line)]
											print "Schwelle Nacht aus der Mail gelesen"
											with open("/home/pi/projects/bda/data/barrier_night.txt","w") as f:
												f.write(barrierNight)
												f.close()
											continue
										
										if line[0:12] == "Tagesbeginn:":
											dayStart = line[13:len(line)]
											print "Tagesbeginn aus der Mail gelesen"
											with open("/home/pi/projects/bda/data/day_start.txt","w") as f:
												f.write(dayStart)
												f.close()	
											continue	
										
										if line[0:12] == "Nachtbeginn:":
											nightStart = line[13:len(line)]
											print "Nachtbeginn aus der Mail gelesen"
											with open("/home/pi/projects/bda/data/night_start.txt","w") as f:
												f.write(nightStart)
												f.close()
											continue
										
										
                                       
            #time.sleep(0.2)
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
	with open('/home/pi/projects/bda/data/time_zwave.pkl', 'rb') as f:
		t = pickle.load(f)
		print(t)
		return t
        
def writeLastTime():
    with open('/home/pi/projects/bda/data/time_zwave.pkl','wb') as f:
		value = time.time()
		#print value
		pickle.dump(value,f)

	
def readBarrierDay():
	f = open('/home/pi/projects/bda/data/barrier_day.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()
	
# In case of error, old value will be stored in the konfigfile
def readBarrierDayOld():
	f = open('/home/pi/projects/bda/data/barrier_day_old.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()
	
def readBarrierDayString():# String, to send the error back to the user
	f = open('/home/pi/projects/bda/data/barrier_day.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return line
	# close the file
	f.close()	

def readBarrierNight():
	f = open('/home/pi/projects/bda/data/barrier_night.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()
	
def readBarrierNightOld():
	f = open('/home/pi/projects/bda/data/barrier_night_old.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()

# For error case
def readBarrierNightString():# String, to send the error back to the user
	f = open('/home/pi/projects/bda/data/barrier_night.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
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
		# The line already has a newline
		# at the end of each line
		return line
	# close the file
	f.close()
	
def readDayStart():
	f = open('/home/pi/projects/bda/data/day_start.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()
	
def readDayStartOld():
	f = open('/home/pi/projects/bda/data/day_start_old.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()

def readDayStartString(): # String, to send the error back to the user
	f = open('/home/pi/projects/bda/data/day_start.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return line
	# close the file
	f.close()
	
def readNightStart():
	f = open('/home/pi/projects/bda/data/night_start.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()
	
def readNightStartOld():
	f = open('/home/pi/projects/bda/data/night_start_old.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return int(line)
	# close the file
	f.close()
	
def readNightStartString(): # String, to send the error back to the user
	f = open('/home/pi/projects/bda/data/night_start.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The line already has a newline
		# at the end of each line
		return line
	# close the file
	f.close()
	
# to initialize the konfiguration values
def writeOpenKitchen():
    with open('/home/pi/projects/bda/data/time_open_kitchen.pkl','wb') as f:
		value = time.time()
		print "open kitchen: ", value
		pickle.dump(value,f)
		
def writeClosedKitchen():
    with open('/home/pi/projects/bda/data/time_closed_kitchen.pkl','wb') as f:
		value = time.time()
		print "closed kitchen: ", value
		pickle.dump(value,f)
            
def writeOpenEntrance():
    with open('/home/pi/projects/bda/data/time_open_entrance.pkl','wb') as f:
		value = time.time()
		print "open entrance: ", value
		pickle.dump(value,f)
		
def writeClosedEntrance():
    with open('/home/pi/projects/bda/data/time_closed_entrance.pkl','wb') as f:
		value = time.time()
		print "closed entrance", value
		pickle.dump(value,f)
#--------------------------------------------------------------
		
# to detect a change in the state of the EnOcean sensor kitchen
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
	
# to detect a change in the state of the EnOcean sensor entrance
def getHasChangedEntrance():
	
	time_open = os.path.getmtime('/home/pi/projects/bda/data/time_open_entrance.pkl')
	time_closed = os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')
	global openOldEntrance
	global closedOldEntrance
	global openedEntrance
	global closedEntrance
	global hasChangedEntrance

	if time_open >= time_closed:
		openedEntrance = True
		closedEntrance = False

	if time_closed >= time_open:
		openedEntrance = False
		closedEntrance = True

	if openOldEntrance == openedEntrance:
		hasChangedEntrance = False
	else:
		hasChangedEntrance = True

	if closedOldEntrance == closedEntrance:
		hasChangedEntrance = False
	else:
		hasChangedEntrance = True
		
	openOldEntrance = openedEntrance
	closedOldEntrance = closedEntrance
	
	return hasChangedEntrance
	
# Simulates an activity at the beginning of the programm. For initialization.
writeOpenKitchen()
time.sleep(0.1)
writeClosedKitchen()
writeOpenEntrance()
time.sleep(0.1)
writeClosedEntrance()
lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')
# ------------------------------------------------------

#def sendError():
#	if errorSchwelleNacht == True:
#		errorSchwelleNacht = False
#		toleranzSchwelleNachtFehler = readSchwelleNachtString()
#		return "Error: " + toleranzSchwelleNachtFehler 


while True:
	print "-------------------NEW-CYCLE----------------"
	print "____________________________________________"
		
	checkMails() # checkMails() called every 30 seconds, because of the following for loop
	
	try:
		dayStart = readDayStart()
		dayStartStr = str(dayStart)
		with open("/home/pi/projects/bda/data/day_start_old.txt","w") as f:			
			f.write(dayStartStr)
			f.close()
		print "Start des Tages: ", dayStart, "Uhr"
	except ValueError:
		errorDayStart = True
		print "   "
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
		print "ERROR: Tagesbeginn konnte nicht gelesen werden. \nFalsche Eingabe!"
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		print "   "
		dayStart = readDayStartOld() # in case of error, old value will be stored
		print "Start des Tages: ", dayStart, "Uhr"
		
	try: 
		nightStart = readNightStart()
		nightStartStr = str(nightStart)
		with open("/home/pi/projects/bda/data/night_start_old.txt","w") as f:			
			f.write(nightStartStr)
			f.close()
		print "Start der Nacht: ", nightStart, "Uhr"
	except ValueError:
		errorNightStart = True
		print "   "
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
		print "ERROR: Nachtbeginn konnte nicht gelesen werden. \nFalsche Eingabe!"
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		print "   "
		nightStart = readNightStartOld()
		print "Start der Nacht: ", nightStart, "Uhr"
	

			
	print "---------------------------------------------"

	mailSendTo = readAddress()
	print "Ziel-Adresse: ", mailSendTo

	try:
		toleranceBarrierDay = readBarrierDay() * 3600 # because of calculating hours to seconds
		toleranceBarrierDayStrOld = str(toleranceBarrierDay / 3600)
		with open("/home/pi/projects/bda/data/barrier_day_old.txt","w") as f:			
			f.write(toleranceBarrierDayStrOld)
			f.close()
		print "Toleranz-Schwelle Tag: ", toleranceBarrierDay / 3600, "Stunden"
	except ValueError:
		errorBarrierDay = True
		print "   "
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
		print "ERROR: Schwelle Tag konnte nicht gelesen werden. \nFalsche Eingabe!"
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		print "   "
		toleranceBarrierDay = readBarrierDayOld() * 3600 # because of calculating hours to seconds
		print "Toleranz-Schwelle Tag: ", toleranceBarrierDay / 3600, "Stunden"
	
	try:
		toleranceBarrierNight = readBarrierNight() * 3600 # because of calculating hours to seconds
		toleranceBarrierNightStrOld = str(toleranceBarrierNight / 3600)
		with open("/home/pi/projects/bda/data/barrier_night_old.txt","w") as f:			
			f.write(toleranceBarrierNightStrOld)
			f.close()
		print "Toleranz-Schwelle Nacht: ", toleranceBarrierNight / 3600, "Stunden"
	except ValueError:
		errorBarrierNight = True
		print "   "
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 
		print "ERROR: Schwelle Nacht konnte nicht gelesen werden. \nFalsche Eingabe!"
		print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		print "   "
		toleranceBarrierNight = readBarrierNightOld() * 3600 # because of calculating hours to seconds
		print "Toleranz-Schwelle Nacht: ", toleranceBarrierNight / 3600, "Stunden"
	print "---------------------------------------------"

		# send state with errors
	if newMails == True:
		print "new mails received"
	
		if errorDayStart == True:
			errorDayStart = False
			dayStartFault = "Fehlerhafte Eingabe ==> Tagesbeginn: " + readDayStartString()
			dayStartStr = str(dayStart)
			with open("/home/pi/projects/bda/data/day_start.txt","w") as f:			
				f.write(dayStartStr)
				f.close()
		else:
			dayStartFault = " "
		
		if errorNightStart == True:
			errorNightStart = False
			nightStartFault = "Fehlerhafte Eingabe ==> Nachtbeginn: " + readNightStartString()
			nightStartStr = str(nightStart)
			with open("/home/pi/projects/bda/data/night_start.txt","w") as f:			
				f.write(nightStartStr)
				f.close()
		else:
			nightStartFault = " "	
		
		if errorBarrierNight == True:
			errorBarrierNight = False
			toleranceBarrierNightFault = "Fehlerhafte Eingabe ==> Schwelle Nacht: " + readBarrierNightString()	
			toleranceBarrierNightStr = str(toleranceBarrierNight)
			with open("/home/pi/projects/bda/data/barrier_night.txt","w") as f:			
				f.write(toleranceBarrierNightStr)
				f.close()
		else:
			toleranceBarrierNightFault = " "
	
		if errorBarrierDay == True:
			errorBarrierDay = False
			toleranceBarrierDayFault = "Fehlerhafte Eingabe ==> Schwelle Tag: " + readBarrierDayString()	
			toleranceBarrierDayStr = str(toleranceBarrierDay)
			with open("/home/pi/projects/bda/data/barrier_day.txt","w") as f:			
				f.write(toleranceBarrierDayStr)
				f.close()
		else:
			toleranceBarrierDayFault = " "
	
		newMails = False
			
		if __name__ == '__main__':
			print "Sende Status"
			sendemail(mailSendFrom, mailSendTo, "Status", "E-Mail: "+mailSendTo+"\n"+"Schwelle Tag: "+str(toleranceBarrierDay)+"\n"+"Schwelle Nacht: "+str(toleranceBarrierNight)+"\n" + "Tagesbeginn: "+str(dayStart)+"\n"+"Nachtbeginn: "+str(nightStart)+"\n----------------------------------------------------"+"\n\n"+str(toleranceBarrierDayFault)+"\n"+str(toleranceBarrierNightFault)+"\n"+str(dayStartFault)+"\n"+str(nightStartFault))
	else:
		print "no new mails received"
	print "---------------------------------------------"
		
		
	# check states of sensors every second for 30 times, then checkMails()
	# check every second, that short changes of the EnOcean sensors cant be detected also.
	# checkMails dont need to bee checked every second.
	for n in range (1,30): # 30 * 1 s sleep
		
			
		# starts LED when door of the house has opened. Clears LED when door is closed.
		# EnOcean Sensor entrance
		if (hasChangedEntrance == True) and (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_open_entrance.pkl')) < 5:
			GPIO.output(8,GPIO.HIGH)
			print "Door open: Hint activated!!!"
			
		if (hasChangedEntrance == True) and (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')) < 5:
			GPIO.output(8,GPIO.LOW)
			print "Door closed: Hint finished"
			
		# taster residentAbsent has been pressed.
		# system is going to sleep now.
		# with this loop it creates time for the resident to leave the house.
		# During this time, no activity wakes up the system.
		# after this time, every activity wakes the system up
		if absent_bool == True and absent_count == True:
			
			for i in range (1,600): # waits 10 minutes (600 * 1 s sleep)
				print "i: ",i
				time.sleep(1)
				#absent_bool = True
				absent_count = False
		#---------------------------------------
	
			
	
	
		# check: is activity
		if os.path.isfile('/home/pi/projects/bda/data/time_zwave.pkl'):
			# time stamp of file (time when last edited)
			lastTimeZWave = os.path.getmtime('/home/pi/projects/bda/data/time_zwave.pkl')
			print "Time of last activity of ZWave: ", lastTimeZWave
		
		getHasChangedKitchen()
		#global actual_time
		if hasChangedKitchen == True:
			#save timestamp of changed 
			if closedKitchen == True:
				lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
			if openedKitchen == True:
				lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
		print "Time of last activity in kitchen:", lastTimeKitchen
	
		getHasChangedEntrance()
		#global actual_time
		if hasChangedEntrance == True:
			#save timestamp of changed 
			if closedEntrance == True:
				lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')
			if openedEntrance == True:
				lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_open_entrance.pkl')
		print "Time of last activity in entrance:" , lastTimeEntrance
		# ------------------------------------------------------------
			
	#Find greatest time:
		if lastTimeZWave >= lastTimeEntrance and lastTimeZWave >= lastTimeEntrance:
			print "ZWave registered last activity"
			lastTime = lastTimeZWave
	
		if lastTimeKitchen >= lastTimeEntrance and lastTimeKitchen >= lastTimeZWave:
			print "Kitchen registered last activity"
			lastTime = lastTimeKitchen
		
		if lastTimeEntrance >= lastTimeKitchen and lastTimeEntrance >= lastTimeZWave:
			print "Entrance registered last activity"
			lastTime = lastTimeEntrance
	#------------------------
	
		
		# Check resident has come home and wake up the system:
		# getHasChangedEntrance()
		# getHasChangedKitchen()
		
		if hasChangedEntrance == True:
			if (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')) < 5:
				# this time has to be greater than the maximal time of one cycle of the whole while loop
				# whithout the for loop that makes the system go sleeping.
				absent_bool = False
			if (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_open_entrance.pkl')) < 5:
				absent_bool = False
		if hasChangedKitchen == True:
			if (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')) < 5:
				absent_bool = False
			if (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')) < 5:
				absent_bool = False
		if (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_zwave.pkl')) < 5:
			absent_bool = False
		#-------------------------------
		
		
		# check day/night
		localtime = time.localtime(time.time()).tm_hour
		print "Aktuelle Stunde: ", localtime

		if localtime >= dayStart and localtime < nightStart: 
			print "It's day"
			day = True
			night = False
			# for detecting a change of the barrier from night to day:
			if night_old != night:
				writeLastTime()
				night_old = False
	
		else:
			print "It's night"
			day = False
			night = True
			night_old = True
		#--------------------------------------------------
		
		if absent_bool == False: #!!!!
		#if GPIO.input(button) == True:
			if day == True:
				print "CHECK TOLERANZ"
				# check Toleranz
				if time.time() - lastTime >= toleranceBarrierDay:
					print "Toleranz-Schwelle Tag ueberschritten"
			
					for i in range (1,6000): # Prealarm for 10 minutes (6000 * 0.1 s sleep) 
						GPIO.output(24,GPIO.HIGH)
					
						getHasChangedEntrance()
						if hasChangedEntrance == True:
						#save timestamp of changed 
							if closedEntrance == True:
								lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')
							if openedEntrance == True:
								lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_open_entrance.pkl')
					
						getHasChangedKitchen()
						if hasChangedKitchen == True:
						#save timestamp of changed 
							if closedKitchen == True:
								lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
							if openedKitchen == True:
								lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
					
					
						# Acknowledge (quittieren) when button or sensor detect activity:
						if ((GPIO.input(acknowledge_button) == True) or (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_zwave.pkl')) < 5 or (time.time() - lastTimeKitchen)< 5 or (time.time() - lastTimeEntrance) < 5):
							print time.time() - lastTimeKitchen
							print time.time() - lastTimeEntrance
							print time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_zwave.pkl')
							print "Warnung quittiert Tag"
							writeLastTime()
						
							break
						print i
						if i == 5999:
							warning = True # Send warning
						time.sleep(0.1) 
			
					GPIO.output(24,GPIO.LOW) # Prealarm stop
			
					if warning == True:
						GPIO.output(24,GPIO.LOW) # Prealarm stop
						writeLastTime()
						warning = False 
						if __name__ == '__main__':
							print "Sende Warnung"
							GPIO.output(25,GPIO.HIGH)
							sendemail(mailSendFrom, mailSendTo, 'Warnung!', 'Hallo\n\nZu wenig Aktivitaet wurde in der Wohnung des Bewohners festgestellt!\nEs kann sein, dass eine Notsituation besteht!\n\nGruesse von der Inaktivitaetserkennung')
							time.sleep(1)
							GPIO.output(25,GPIO.LOW)
	
		if absent_bool == False:
			if night == True:
				print "CHECK TOLERANZ"
				if time.time() - lastTime >= toleranceBarrierNight:
					print "Toleranz-Schwelle Nacht ueberschritten"
			
					for i in range (1,6000):# Prealarm for 10 minutes (6000 * 0.1 s sleep)
						GPIO.output(24,GPIO.HIGH)
					
						getHasChangedEntrance()
						if hasChangedEntrance == True:
						#save timestamp of changed 
							if closedEntrance == True:
								lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_closed_entrance.pkl')
							if openedEntrance == True:
								lastTimeEntrance = os.path.getmtime('/home/pi/projects/bda/data/time_open_entrance.pkl')
					
						getHasChangedKitchen()
						if hasChangedKitchen == True:
						#save timestamp of changed 
							if closedKitchen == True:
								lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_closed_kitchen.pkl')
							if openedKitchen == True:
								lastTimeKitchen = os.path.getmtime('/home/pi/projects/bda/data/time_open_kitchen.pkl')
					

						# Acknowledge (quittieren) when button or sensor detect activity:
						if ((GPIO.input(acknowledge_button) == True) or (time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_zwave.pkl')) < 5 or (time.time() - lastTimeKitchen)< 5 or (time.time() - lastTimeEntrance) < 5):
							print time.time() - lastTimeKitchen
							print time.time() - lastTimeEntrance
							print time.time() - os.path.getmtime('/home/pi/projects/bda/data/time_zwave.pkl')
							print "Warnung quittiert nacht"
							writeLastTime()
							break
						print i
						if i == 5999: 
							warning = True # Send warning
						time.sleep(0.1) 
			
					GPIO.output(24,GPIO.LOW) # Prealarm stop
			
					if warning == True:
						GPIO.output(24,GPIO.LOW) # Prealarm stop
						writeLastTime()
						warning = False 
						if __name__ == '__main__':
							print "Sende Warnung"
							GPIO.output(25,GPIO.HIGH)
							sendemail(mailSendFrom, mailSendTo, 'Warnung!', 'Hallo\n\nZu wenig Aktivitaet wurde in der Wohnung des Bewohners festgestellt!\nEs kann sein, dass eine Notsituation besteht!\n\nGruesse von der Inaktivitaetserkennung')
							time.sleep(1)
							GPIO.output(25,GPIO.LOW)
		print "n: ",n		
				
		time.sleep(1)
					
	time.sleep(1) 
		


		
