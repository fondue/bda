#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015


import os #for os.system
import time

def writeLastTime():
    with open('/home/pi/projects/bda/data/zwave_time.txt','w') as f:
		value = time.time()
		print value
		f.write(str(value))
		f.close()

		
		
writeLastTime()






