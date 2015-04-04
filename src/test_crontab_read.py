#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
# Um crontab zu testen

import time, os
import pickle

def readLastTime():
    with open("../data/test_datei.pkl","rb") as f:
        t = pickle.load(f)
        print(t)
        return t
       
readLastTime()
