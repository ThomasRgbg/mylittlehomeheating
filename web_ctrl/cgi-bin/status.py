#!/usr/bin/env python

import cgi
import cgitb

from .. import heiz_ctrl.heizctrl.ctrl

from subprocess import call, Popen

cgitb.enable()

arguments = cgi.FieldStorage()

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title> Heizung </title>"
print "</head>"
print "<body>"


print("<p> Status: </p>")


print "</body>"
print "</html>"




