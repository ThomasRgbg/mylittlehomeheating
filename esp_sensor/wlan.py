# 
# WLAN / Network related functions

import network
import ntptime
import time

password = ''

class mywlan(object):
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        self.ap_if = network.WLAN(network.AP_IF)
        self.sta_if.active(False)
        self.ap_if.active(False)
        self.synccount=0

    def connect(self):
        start = time.ticks_ms()
        print("Connect wlan")
        if not self.sta_if.isconnected():
            self.sta_if.active(True)
            self.sta_if.connect('thomasssid', password)

        self.synccount += 1
        while (time.ticks_diff(time.ticks_ms(), start) < 5000):
            if self.sta_if.isconnected() and (time.time() < 536962532 or self.synccount > 50):
                try:
                    print("Sync Time via NTP")
                    ntptime.settime()
                    self.synccount = 0
                except OSError:
                    # It nis not critical, if time is not synced, since 
                    # he will do this with next send loop.
                    pass
                break
        if self.sta_if.isconnected():
            print("Wlan connected")
        else:
            print("Wlan NOT connected")

    def isconnected(self):
        return self.sta_if.isconnected()

    def off(self):
        print("Disconnect wlan")
        self.sta_if.active(False)
