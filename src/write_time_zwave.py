#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# only writes zero to the file. Then the logical part of the 
# system reads the time of the last editing.

import pickle

def writeLastTime():
    with open('/home/pi/projects/bda/data/time_zwave.pkl','wb') as f:
		value = 0
		pickle.dump(value,f)
		
writeLastTime()






