#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys

con = lite.connect('/var/lib/temperatur/temperatur.db')

with con:
    
    cur = con.cursor()    
    
    cur.execute("DROP TABLE IF EXISTS Temperatur")
    cur.execute("CREATE TABLE Temperatur(Timestamp TIMESTAMP, TempVorlauf REAL, TempRuecklauf REAL, TempVorne REAL, TempHinten REAL, TempBoden REAL, TempLuft REAL)")
