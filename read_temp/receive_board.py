#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep, localtime, strftime

import sqlite3
import datetime
import logging
import sys
import os
import socket

from optparse import OptionParser

if __name__== "__main__":
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                     action='store_const', dest='loglevel',
                     const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                     action='store_const', dest='loglevel',
                     const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                     action='store_const', dest='loglevel',
                     const=5, default=logging.INFO)

    optp.add_option("-l", "--logfile", dest="logfile",
                    help="logfile to use")

    opts, args = optp.parse_args()

    if opts.logfile is not None:
        if sys.version_info < (3, 0):
            console_log = open(opts.logfile, 'a', 1)
        else:
            console_log = open(opts.logfile, 'a', 1, encoding='utf-8')
        sys.stdout = console_log
        sys.stderr = console_log

    # Setup logging.
    logging.basicConfig(level = opts.loglevel, datefmt='%H:%M:%S', format='%(asctime)s %(levelname)s:%(name)s:%(funcName)s:%(message)s')
    logger = logging.getLogger(__name__)

    logger.debug(opts)

    # Data storage
    sqlcon = sqlite3.connect('/var/lib/temperatur/temperatur.db')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind( ('',6666) )
    s.listen(1)

    command = 'nosleep'

    while True:

        logger.debug( "wait for connect")
        conn, addr = s.accept()
        logger.debug('Connection address: {0} at {1}'.format(addr,datetime.datetime.now()) )
        while True:
            data = conn.recv(1024)
            if not data: break
            data = data.split(',')
            logger.debug('received data [{0}]: {1}'.format(len(data), data) )
            if (5 % (len(data) + 5))  == 5:

                for i in range( (len(data)) / 5):
                    timestamp = datetime.datetime.fromtimestamp(int(data[i*5 + 1]))
                    timestamp = timestamp.replace(day=timestamp.day-1, year = timestamp.year + 30)

                    temp1 = float(data[i*5 + 2])
                    if temp1 == -254.0: temp1 = None

                    temp2 = float(data[i*5 + 3])
                    if temp2 == -254.0: temp2 = None

                    temp3 = float(data[i*5 + 4])
                    if temp3 == -254.0: temp3 = None

                    logger.debug('Got Data: [{0}] 1: {1}, 2: {2}, 3: {3}'.format(timestamp,temp1,temp2,temp3))

                    temps = [1, None, None, None, temp1, temp2, temp3]
                    temps[0] = timestamp

                    logger.debug("Write into db: {0}".format(temps))

                    # convert (back) to tuple for sqlite3
                    ttemps = tuple(temps)

                    # Table:
                    # cur.execute("CREATE TABLE Temperatur(Timestamp INT, TempVorlauf REAL, TempRuecklauf REAL, TempVorne REAL, TempHinten REAL, TempBoden REAL, TempLuft REAL)")
                    with sqlcon:
                        cur = sqlcon.cursor()
                        cur.executemany("INSERT INTO Temperatur VALUES(?, ?, ?, ?, ?, ?, ?)", (ttemps,) ) # Important: (foo,)

                response = str(len(data)/5) + ","

            else:
                response = '0,'

            response += command

            logger.debug("Responding: {0}".format(response))
            conn.sendall(response)
            conn.close()
            break



