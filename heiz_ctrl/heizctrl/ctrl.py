#!/usr/bin/python

import sys
from time import sleep, strftime
from datetime import datetime, timedelta


import pifacedigitalio

from .cron import HeizungCronControl

class HeizungControl(HeizungCronControl):


    def heizung_create_token(self, channel, duration):

        endtime = datetime.now() + timedelta(seconds=duration*60)
        print("create token valid until {0}".format(endtime))

        file = open('/var/lock/heizung_token.txt', 'w')
        file.write('%d,%s\n'% (channel, endtime.strftime("%Y,%m,%d,%H,%M,%S") ) )
        file.flush()
        file.close()


    def heizung_1ch_on(self, channel):
        pfd = pifacedigitalio.PiFaceDigital()

        pfd.output_pins[0].value=1 # "Schlafzimmer" (Buero)
        pfd.output_pins[1].value=1 # "Kinderzimmer" (Schlafzimmer)
        pfd.output_pins[2].value=1 # Bad
        pfd.output_pins[3].value=1 # Wohnzimmer
        sleep(0.1)
        pfd.output_pins[channel].value=0

        logger.info("State of Piface: {:08b} ".format(pfd.output_port.value))

    def heizung_1ch(self, channel, duration):
        self.heizung_create_token(channel, duration)
        # self.heizung_1ch_on(channel)

        self.add_off_event(datetime.now(), channel, duration)




