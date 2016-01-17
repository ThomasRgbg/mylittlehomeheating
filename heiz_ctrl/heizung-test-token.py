#!/usr/bin/python

# This file should be called periodically, e.g. in cron.hourly to check for stuck events. 

import csv
import datetime
import sys
import os

from heizctrl.ctrl import HeizungControl


tokenfile = "/var/lock/heizung_token.txt"
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

def clean_tokenfile():
    open(tokenfile,'w').close()

cleanup = False

# logprint("Testing Token")

if os.path.isfile(tokenfile):
    os.chown(tokenfile,1000,1000)
    with open(tokenfile, 'rb') as f:
        reader = csv.reader(f)
        # print reader
        for row in reader:
    
            re = len(row)
            timestamp = datetime.datetime(year=int(row[re-6]), month=int(row[re-5]), day=int(row[re-4]), hour=int(row[re-3]), minute=int(row[re-2]), second=int(row[re-1]) )

            t1 = int(row[0])

            logprint('Found: Timestamp {0} Channel: {1}'.format(timestamp, t1))

            # Timestamp > 1h in future should not happen
            if timestamp - datetime.timedelta(seconds=3600) > now:
                logprint("Event more than 1h in future - cleanup")
                cleanup = True
    
            # Old timestamp left
            elif timestamp < now:
                logprint("Old event detected - cleanup")
                cleanup = True

            # Timestamp between now and 1h away - let it run
            else:
                logprint("Found running event - no cleanup")
                cleanup = False

else: 
    logprint("Token file does not exist")


logprint("State cleanup: {0}".format(cleanup))

if cleanup:
    heizung = HeizungControl()
    heizung.heizung_all_off()
    clean_tokenfile()

