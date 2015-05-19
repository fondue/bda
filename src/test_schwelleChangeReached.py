#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# 

import time



# check change of schwelle
# global variable will be set after call of function

schwelleChangeReached = False
tag = True
nacht = False
localtime = time.localtime(time.time()).tm_min
tagStartInitInt = 8
nachtStartInitInt = 37

print localtime

if localtime >= tagStartInitInt and localtime < nachtStartInitInt:
	print "It's day Init"
	tag = True
	nacht = False
	oldTag = True
		
else:
	print "It's night Init"
	tag = False
	nacht = True
	oldTag = False

def getSchwelleChangeReached():

	global schwelleChangeReached
	global tag
	global nacht
	global oldTag
	global oldNacht
	
	if time.localtime(time.time()).tm_min >= tagStartInitInt and time.localtime(time.time()).tm_min < nachtStartInitInt:
			tag = True
		
	else:
			tag = False
		
	if oldTag == tag:
		 schwelleHasChanged = False
	else:
		 schwelleHasChanged = True
		
	oldTag = tag
	return schwelleChangeReached


while True:
	
	getSchwelleChangeReached()
	localtime = time.localtime(time.time()).tm_min
	print localtime
	print "Schwelle change reached: ", schwelleChangeReached
	#print "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
	time.sleep(1)
