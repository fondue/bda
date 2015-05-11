#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015

import pickle
import os
import time

openOld = True
closedOld = False
actual_time = os.path.getmtime('/home/pi/projects/bda/data/time_open.pkl')

while True:
	
	time_open = os.path.getmtime('/home/pi/projects/bda/data/time_open.pkl')
	time_closed = os.path.getmtime('/home/pi/projects/bda/data/time_closed.pkl')
	

	if time_open >= time_closed:
		open = True
		closed = False

	if time_closed >= time_open:
		open = False
		closed = True




	if openOld == open:
		hasChanged = False
	else:
		hasChanged = True

	if closedOld == closed:
		hasChanged = False
	else:
		hasChanged = True


	openOld = open
	closedOld = closed


	if hasChanged == True:
		#save timestamp of changed 
		if time_closed >= time_open:
			actual_time = os.path.getmtime('/home/pi/projects/bda/data/time_closed.pkl')
		if time_open >= time_closed:
			actual_time = os.path.getmtime('/home/pi/projects/bda/data/time_open.pkl')
			
	if time.time() - actual_time >= 5:
		print "Warnung!"
		actual_time = time.time()
	
	print "actual time: " + str(actual_time)
	time.sleep(1)
			
			
			
			
			
			
			
			
