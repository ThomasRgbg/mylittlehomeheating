#!/usr/bin/python
# -*- coding: utf-8 -*-

from smbus import SMBus
from time import sleep, localtime, strftime

import sqlite3
import datetime




class thermometer(object):

    def __init__(self, i2caddr):
	self.i2caddr = i2caddr
	self.delay = 4
	self.average = 2
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
	    # print ("0x%x" % self.i2caddr), i, temp_f, ("0x%x" % reg5)
	    if temp_f <= 0 or temp_f > 60:
		average -= 1
	    else:
		temper += temp_f
	    sleep(self.delay)

	if average == 0:
	    temper = self.last_value
	else:
	    temper /= (average)
	    self.last_value = temper
	# print self.i2caddr, "A", temper
	return temper


i2c = SMBus(1)

thermo_luft = thermometer(i2caddr=0x19)
thermo_vorlauf = thermometer(i2caddr=0x18)
thermo_ruecklauf = thermometer(i2caddr=0x1e)
sqlcon = sqlite3.connect('/var/lib/temperatur/temperatur.db')


while True:

    # temp_luft = 1
    temp_luft = thermo_luft.get_temp()
    temp_vorlauf = thermo_vorlauf.get_temp()
    temp_ruecklauf = thermo_ruecklauf.get_temp()

#     file.write('%3.2f,%3.2f,%3.2f,%s\n'% (temp_luft, temp_vorlauf, temp_ruecklauf, strftime("%Y,%m,%d,%H,%M,%S",localtime() ) ) )
#     file.flush()

    temps = [1, temp_vorlauf, temp_ruecklauf, temp_luft, None, None, None]
    temps[0] = datetime.datetime.now()

    # convert (back) to tuple
    ttemps = tuple(temps)
#    print temps

    # Table:
    # cur.execute("CREATE TABLE Temperatur(Timestamp INT, TempVorlauf REAL, TempRuecklauf REAL, TempVorne REAL, TempHinten REAL, TempBoden REAL, TempLuft REAL)")
    with sqlcon:
        cur = sqlcon.cursor()
        cur.executemany("INSERT INTO Temperatur VALUES(?, ?, ?, ?, ?, ?, ?)", (ttemps,) ) # Important: (foo,)

    sleep(60 - (24))











