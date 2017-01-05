# 
# WLAN / Network related functions

import network
import ntptime
import time

password = ''

class mywlan(object):
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)

    def connect(self):
        self.sta_if.active(True)
        self.sta_if.connect('thomasssid', password)

        start = time.ticks_ms()
    
        while (time.ticks_diff(time.ticks_ms(), start) < 5000):
            if self.sta_if.isconnected() and time.time() < 536962532:
                try:
                    print("Sync Time via NTP")
                    ntptime.settime()
                except OSError:
                    # It nis not critical, if time is not synced, since 
                    # he will do this with next send loop.
                    pass
                break

    def isconnected(self):
        return self.sta_if.isconnected()

    def off(self):
        self.sta_if.active(False)
