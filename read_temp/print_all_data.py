#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys


con = lite.connect('/var/lib/temperatur/temperatur.db')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM Temperatur")

    rows = cur.fetchall()

    for row in rows:
        print row