#!/usr/bin/python
# -*- coding: utf-8 -*-

# import csv
import sqlite3 as lite
import datetime

import matplotlib.dates
from matplotlib.figure import Figure
# from matplotlib.patches import Polygon
from matplotlib.backends.backend_agg import FigureCanvasAgg
# import matplotlib.numerix as nx
from matplotlib import rc
from numpy import nan


class temperaturdata(object):
    def __init__(self):
        self.temp1 = []
        self.temp2 = []
        self.temp3 = []
        self.temp4 = []
        self.temp5 = []
        self.temp6 = []
        self.timestamps = []

def find_val(values, value):
    return [i for i,x in enumerate(values) if value != x]

def remove_in(values, pos):
    #return [x for i,x in enumerate(values) if i in pos]
    return [values[x] for x in pos]

def remove_none(x,y):
    pos = find_val(y, None)
    x2 = remove_in(x, pos)
    y2 = remove_in(y, pos)
    return (x2, y2)

def dezimate(x, y, dez):
    x1=[]
    y1=[]
    for i in range(len(x)/ dez):
        z=0
        for j in range(dez):
            z += x[i*dez+j]
        x1.append( z/dez )
        z=0
        for j in range(dez):
            z += y[i*dez+j]
        y1.append( z/dez )
    

    return (x1, y1)

def import_data(days=1):
    tdata = temperaturdata()
    con = lite.connect('/var/lib/temperatur/temperatur.db')
    con.execute("PRAGMA busy_timeout = 60000")   # 60 s

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

            tdata.temp1.append(t1)
            tdata.temp2.append(t2)
            tdata.temp3.append(t3)
            tdata.temp4.append(t4)
            tdata.temp5.append(t5)
            tdata.temp6.append(t6)
            tdata.timestamps.append(timestamp)
    return (tdata)




def create_plot(tdata, outputfile):
    times = matplotlib.dates.date2num(tdata.timestamps)    

    points = 400

#    print len(times1)

    rc('xtick', labelsize=8)
    rc('ytick', labelsize=8)

    fig = Figure(figsize=(8,8))
#    ax = fig.add_subplot(211)
#    bx = fig.add_subplot(212)
    ax = fig.add_subplot(311)
    bx = fig.add_subplot(312)
    cx = fig.add_subplot(313)

    (x1,y1) = remove_none(times, tdata.temp3)
    if len(x1) != 0:
        (x1,y1) = dezimate(x1,y1,int(len(x1) / points))
        ax.plot_date(x1, y1 , xdate=True, ydate=False, linestyle='-', marker='', color='b', label='Vorne')

    (x2,y2) = remove_none(times, tdata.temp4)
    if len(x2) != 0:
        (x2,y2) = dezimate(x2,y2,int(len(x2) / points))
        ax.plot_date(x2, y2,  xdate=True, ydate=False, linestyle='-', marker='', color='g', label='Gummibaum')

    ax.legend(loc=2, prop={'size':7})
    ax.grid()

    (x1,y1) = remove_none(times, tdata.temp1)
    if len(x1) != 0:
        (x1,y1) = dezimate(x1,y1,int(len(x1) / points))
        bx.plot_date(x1, y1, xdate=True, ydate=False, linestyle='-', marker='', color='r', label='Zulauf')

    (x2,y2) = remove_none(times, tdata.temp2)  
    if len(x2) != 0:
        (x2,y2) = dezimate(x2,y2,int(len(x2) / points))
        bx.plot_date(x2, y2, xdate=True, ydate=False, linestyle='-', marker='', color='g', label='Ruecklauf')

    bx.legend(loc=2, prop={'size':7})
    bx.grid()

    (x1,y1) = remove_none(times, tdata.temp5)
    if len(x1) != 0:
        (x1,y1) = dezimate(x1,y1,int(len(x1) / points))
        cx.plot_date(x1, y1, xdate=True, ydate=False, linestyle='-', marker='', color='k', label='Boden')

    (x2,y2) = remove_none(times, tdata.temp6)  
    if len(x2) != 0:
        (x2,y2) = dezimate(x2,y2,int(len(x2) / points))
        cx.plot_date(x2, y2, xdate=True, ydate=False, linestyle='-', marker='', color='b', label='Zuluft')

    cx.legend(loc=2, prop={'size':7})
    cx.grid()

    # ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d:%m'))
    fig.autofmt_xdate()

    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outputfile, dpi=180)


if __name__ == "__main__":
    # print "a"
    tdata = import_data(days=1)
    create_plot(tdata, "/var/www/html/temperatur/1days.png")
    tdata = import_data(days=2)
    # print len(tdata.temp1)
    create_plot(tdata, "/var/www/html/temperatur/2days.png")
    # tdata = import_data(days=7)
    # print len(tdata.temp1)
    # create_plot(tdata, "/var/www/html/temperatur/7days.png", 64)








