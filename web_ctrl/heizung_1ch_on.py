#!/usr/bin/python

import sys
from time import sleep, strftime
from datetime import datetime, timedelta

import pifacedigitalio

logfile = open('/var/log/heizung_control.log', 'ab', 0)

def log(string):
    timestamp = (datetime.now()).strftime('%Y.%m.%d %H:%M:%S ')
    logfile.write(timestamp + string.encode('utf-8') + '\n' )
    logfile.flush()

def logprint(string):
    log(string)
    print string


def heizung_create_token(channel, duration):

    endtime = datetime.now() + timedelta(seconds=duration*60)

    file = open('/var/lock/heizung_token.txt', 'w')
    file.write('%d,%s\n'% (channel, endtime.strftime("%Y,%m,%d,%H,%M,%S") ) )
    file.flush()
    file.close()


def heizung_1ch_on(channel):
    pfd = pifacedigitalio.PiFaceDigital()

    pfd.output_pins[0].value=1 # "Schlafzimmer" (Buero)
    pfd.output_pins[1].value=1 # "Kinderzimmer" (Schlafzimmer)
    pfd.output_pins[2].value=1 # Bad
    pfd.output_pins[3].value=1 # Wohnzimmer
    sleep(0.1)
    pfd.output_pins[channel].value=0

    logprint("State of Piface: {:08b} ".format(pfd.output_port.value))



if len(sys.argv) != 3:
    logprint("Incorrect arguments")
    logprint("Usage:  heizung_1ch_on.py <channel> <duration minutes>")
    sys.exit(1)

logprint("heizung_1ch_on.py")

channel = int(sys.argv[1])
duration = int(sys.argv[2])

logprint("Heizung channel: {0}, duration {1}".format(channel,duration))

heizung_create_token(channel, duration )

heizung_1ch_on(channel)

