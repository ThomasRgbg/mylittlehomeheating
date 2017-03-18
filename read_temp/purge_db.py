#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime

keepdays = 7

con = lite.connect('/var/lib/temperatur/temperatur.db')

t_old = [ datetime.datetime.now() - datetime.timedelta(days=keepdays/2.0) ]
tt_old = tuple(t_old)
# print tt_old

with con:
    cur = con.cursor()    
    cur.execute("DELETE FROM Temperatur WHERE timestamp < ?", tt_old )
    con.commit()


