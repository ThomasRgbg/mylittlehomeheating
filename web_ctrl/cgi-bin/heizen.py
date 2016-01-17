#!/usr/bin/env python

import cgi
import cgitb

from subprocess import call, Popen

cgitb.enable()

arguments = cgi.FieldStorage()

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title> Heizung </title>"
print "</head>"
print "<body>"

ort = None
zeit = None

for i in arguments.keys():
    if arguments[i].name == 'ort':
        ort = arguments[i].value
    if arguments[i].name == 'zeit':
        zeit = arguments[i].value

if ort != None and zeit != None:
    print("<p> Ort {0}</p>".format(ort))
    print("<p> Zeit {0}</p>".format(zeit))

    if ort=='bad':
        call(["heizung_1ch_on.py",'-c','2','-t',zeit,'-l','/var/log/heiz_ctrl.log'])
    elif ort=='wohnzimmer':
        call(["heizung_1ch_on.py",'-c','3','-t',zeit,'-l','/var/log/heiz_ctrl.log'])
    elif ort=='arbeitszimmer':
        call(["heizung_1ch_on.py",'-c','0','-t',zeit,'-l','/var/log/heiz_ctrl.log'])
    elif ort=='schlafzimmer':
        call(["heizung_1ch_on.py",'-c','1','-t',zeit,'-l','/var/log/heiz_ctrl.log'])
    else:
        call(["heizung_all_off.py",'-l','/var/log/heiz_ctrl.log'])

else:
    print("<p> Error: </p>")
    if ort == None:
        print("<p> Ort missing <p>")
    if zeit == None:
        print("<p> Zeit missing <p>")

print "</body>"
print "</html>"




