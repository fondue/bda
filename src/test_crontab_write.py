#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# Um die crontab zu testen

import pickle
import time, os #for crontab


def writeLastTime():
	test = time.time()
	print time.time()
	file = open("../data/test_datei.pkl","wb")
	pickle.dump(test,file)
	file.close()
	
writeLastTime()
