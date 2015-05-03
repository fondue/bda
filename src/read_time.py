#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# Um die crontab zu testen

#import pickle
#import time, os #for crontab
import time




def read():
	f = open('/home/pi/projects/bda/data/last_time.txt')
	while True:
		line = f.readline()
		# Zero length indicates EOF
		if len(line) == 0:
			break
		# The `line` already has a newline
		# at the end of each line
		# since it is reading from a file.
		print line,
	# close the file
	f.close()
	
	
read()
