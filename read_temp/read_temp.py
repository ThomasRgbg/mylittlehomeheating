#!/usr/bin/python
# -*- coding: utf-8 -*-

from smbus import SMBus
from time import sleep, localtime, strftime

import sqlite3
import datetime
import logging
import os

import cronus.beat as beat

from optparse import OptionParser

class thermometer(object):

    def __init__(self, i2caddr, name=''):
	self.logger = logging.getLogger(__name__)
	self.i2caddr = i2caddr
	self.name = name

	self.delay = 4     # Delay between reads (sec)
	self.average = 2   # How often read
	self.last_value = 0

    def get_temp(self):
        temper = 0
        average = self.average

        for i in range(self.average):
	    try:
		reg5 = i2c.read_word_data(self.i2caddr, 0x05)
	    except (IOError):
		reg5 = 0
	    temp = (reg5 & 0x0f) * 0x100 + (reg5 & 0xff00) / 0xff
	    temp_f = float(temp) / float(0x10)
	    self.logger.debug("read 0x{0:x}, {1}, {2}, 0x{3:x}".format(self.i2caddr, i, temp_f, reg5))

	    # Only add if reasonable temperatur (I2C might be unreliable)
	    if temp_f <= 0 or temp_f > 60:
		average -= 1
	    else:
		temper += temp_f

	    sleep(self.delay)

	# FIXME: If no values at all usable, use last value
	if average == 0:
	    temper = self.last_value
	else:
	    temper /= (average)
	    self.last_value = temper

	self.logger.info("Result: Name: {0}, i2c: 0x{1:x}, Temp: {2}".format(self.name, self.i2caddr, temper))
	return temper

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

    i2c = SMBus(1)

    thermo_luft = thermometer(i2caddr=0x19, name='Luft vorne')
    thermo_vorlauf = thermometer(i2caddr=0x18, name='Vorlauf')
    thermo_ruecklauf = thermometer(i2caddr=0x1e, name='Ruecklauf')

    beat.set_rate(1.0/60)

    while beat.true():
        temp_luft = thermo_luft.get_temp()
        temp_vorlauf = thermo_vorlauf.get_temp()
        temp_ruecklauf = thermo_ruecklauf.get_temp()

        temps = [1, temp_vorlauf, temp_ruecklauf, temp_luft, None, None, None]
        temps[0] = datetime.datetime.now()

        logger.debug("Write into db: {0}".format(temps))

        # convert (back) to tuple for sqlite3
        ttemps = tuple(temps)

        # Table:
        # cur.execute("CREATE TABLE Temperatur(Timestamp INT, TempVorlauf REAL, TempRuecklauf REAL, TempVorne REAL, TempHinten REAL, TempBoden REAL, TempLuft REAL)")
        with sqlcon:
            sqlcon.execute("PRAGMA busy_timeout = 60000")   # 60 s
            cur = sqlcon.cursor()
            cur.executemany("INSERT INTO Temperatur VALUES(?, ?, ?, ?, ?, ?, ?)", (ttemps,) ) # Important: (foo,)

        logger.debug("Wait for next turn")
        beat.sleep()



