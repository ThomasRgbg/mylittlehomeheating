#!/usr/bin/python

import pifacedigitalio
import datetime

logfile = open('/var/log/heizung_control.log', 'ab', 0)

def log(string):
    timestamp = (datetime.datetime.now()).strftime('%Y.%m.%d %H:%M:%S ')
    logfile.write(timestamp + string.encode('utf-8') + '\n' )
    logfile.flush()

def logprint(string):
    log(string)
    print string

def clean_tokenfile():
    open('/var/lock/heizung_token.txt', 'w').close()

logprint("heizung_all_off.py")

pfd = pifacedigitalio.PiFaceDigital() 
pfd.output_pins[0].value=1 # "Schlafzimmer" (Buero)
pfd.output_pins[1].value=1 # "Kinderzimmer" (Schlafzimmer)
pfd.output_pins[2].value=1 # Bad
pfd.output_pins[3].value=1 # Wohnzimmer

logprint("State of Piface: {:08b} ".format(pfd.output_port.value))

clean_tokenfile()

