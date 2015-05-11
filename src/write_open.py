#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015


import os #for os.system
import time
import pickle

def writeLastTime():
    with open('/home/pi/projects/bda/data/time_open.pkl','wb') as f:
		value = time.time()
		print value
		pickle.dump(value,f)
		#value = time.time()
		#print value
		#f.write(str(value))
		#f.close()

		
writeLastTime()
