#!/usr/bin/python
# v0.1 by Dominik Imhof 05.2015
# only writes zero to the file. Then the logical part of the 
# system reads the time of the last editing.

import pickle

def writeLastTime():
    with open('/home/pi/projects/bda/data/time_closed_entrance.pkl','wb') as f:
		value = 0
		pickle.dump(value,f)
		
writeLastTime()
