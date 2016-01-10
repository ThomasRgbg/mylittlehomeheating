#!/usr/bin/python

import csv
import datetime
import sys
import pifacedigitalio
import os

inputfile = "/var/lock/heizung_token.txt"
logfile = open('/var/log/heizung_test_token.log', 'ab', 0)

now = datetime.datetime.now()


def log(string):
    timestamp = (datetime.datetime.now()).strftime('%Y.%m.%d %H:%M:%S ')
    logfile.write(timestamp + string.encode('utf-8') + '\n' )
    logfile.flush()

def logprint(string):
    log(string)

    if len(sys.argv) == 2:
        if sys.argv[1] == '-v':
            print string

def heizung_all_off():

    logprint("Switch all off")
    pfd = pifacedigitalio.PiFaceDigital() 

    pfd.output_pins[0].value=1 # "Schlafzimmer" (Buero)
    pfd.output_pins[1].value=1 # "Kinderzimmer" (Schlafzimmer)
    pfd.output_pins[2].value=1 # Bad
    pfd.output_pins[3].value=1 # Wohnzimmer

    logprint("State of Piface: {:08b} ".format(pfd.output_port.value))

def clean_inputfile():
    open(inputfile,'w').close()

cleanup = True

logprint("Testing Token")

if os.path.isfile(inputfile):
    os.chown(inputfile,1000,1000)
    with open(inputfile, 'rb') as f:
        reader = csv.reader(f)
        # print reader
        for row in reader:
    
            re = len(row)
            timestamp = datetime.datetime(year=int(row[re-6]), month=int(row[re-5]), day=int(row[re-4]), hour=int(row[re-3]), minute=int(row[re-2]), second=int(row[re-1]) )

            t1 = int(row[0])

            logprint('{0} : {1}'.format(timestamp, t1))

            # Timestamp > 1h in future should not happen
            if timestamp - datetime.timedelta(seconds=3600) > now:
                logprint("Event more than 1h in future - cleanup")
    
            # Old timestamp left
            elif timestamp < now:
                logprint("Old event detected - cleanup")

            # Timestamp between now and 1h away - let it run
            else:
                logprint("Found running event - no cleanup")
                cleanup = False

else: 
    logprint("Token file does not exist")


logprint("State cleanup: {0}".format(cleanup))

if cleanup:
    heizung_all_off()
    clean_inputfile()

