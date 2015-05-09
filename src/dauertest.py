#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 

import time
import os
import pickle

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

toleranzSchwelle = 3600 # 4 Stunden

while True:
	
	print "Dauertest gestartet"
	lastTime = os.path.getmtime('/home/pi/projects/bda/data/last_time.pkl')
	if time.time() - lastTime >= toleranzSchwelle:
		writeLog()
		print "Zeit notiert"
		writeLastTime()
	time.sleep(800)
