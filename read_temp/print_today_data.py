#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime

class temperaturdata(object):
    def __init__(self):
        self.temp1 = []
        self.temp2 = []
        self.temp3 = []
        self.temp4 = []
        self.temp5 = []
        self.temp6 = []
        self.timestamps = []


def import_data(days=1):
    tdata = temperaturdata()
    con = lite.connect('/var/lib/temperatur/temperatur.db')

    t_old = [ datetime.datetime.now() - datetime.timedelta(days=days) ]
    tt_old = tuple(t_old)
    # print tt_old

    with con:
        cur = con.cursor()    
        cur.execute("SELECT * FROM Temperatur WHERE timestamp > ?", tt_old )
        rows = cur.fetchall()

        for row in rows:

            tstamp,t1,t2,t3,t4,t5,t6 = row

            timestamp = datetime.datetime.strptime(tstamp[0:19], "%Y-%m-%d %H:%M:%S")
            #timestamp = datetime.datetime.strptime(tstamp, "%Y-%m-%d %H:%M:%S.%f")

            tdata.temp1.append(t1)
            tdata.temp2.append(t2)
            tdata.temp3.append(t3)
            tdata.temp4.append(t4)
            tdata.temp5.append(t5)
            tdata.temp6.append(t6)
            tdata.timestamps.append(timestamp)
    return (tdata)


data = import_data(days=1)

for row in range(len(data.timestamps)):
    print(data.timestamps[row], data.temp1[row], data.temp2[row], data.temp3[row], data.temp4[row], data.temp5[row], data.temp6[row])



