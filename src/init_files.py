#!/usr/bin/python
# v0.1 by Dominik Imhof 03.2015
#


# Initialisiere Dateien

address_init = "dominik.imhof@stud.hslu.ch"
with open("/home/pi/projects/bda/data/address.txt","w") as f:
	f.write(address_init+"\n")
	f.close()
	
schwelleTag_init = "15"
with open("/home/pi/projects/bda/data/schwelle_tag.txt","w") as f:
	f.write(schwelleTag_init+"\n")
	f.close()

schwelleNacht_init = "12"
with open("/home/pi/projects/bda/data/schwelle_nacht.txt","w") as f:
	f.write(schwelleNacht_init+"\n")
	f.close()
								
tagesbeginn_init = "7"
with open("/home/pi/projects/bda/data/tages_beginn.txt","w") as f:
	f.write(tagesbeginn_init+"\n")
	f.close()		

nachtbeginn_init = "23"
with open("/home/pi/projects/bda/data/nacht_beginn.txt","w") as f:
	f.write(nachtbeginn_init+"\n")
	f.close()	
