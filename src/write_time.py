#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# Um die crontab zu testen

#import pickle
import time, os #for crontab


def writeLastTime():
	test = time.time()
	print time.time()
	with open("/home/pi/projects/bda/data/last_time.txt","w") as f:
		f.write(str(test))
		f.close()
	
writeLastTime()
