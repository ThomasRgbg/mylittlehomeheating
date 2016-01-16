#!/usr/bin/python

import sys
from time import sleep, strftime
from datetime import datetime, timedelta


import pifacedigitalio

from .cron import HeizungCronControl

class HeizungControl(HeizungCronControl):
    def __init__(self, init_board=False):
        self.pfd = pifacedigitalio.PiFaceDigital(init_board=init_board)

    def heizung_create_token(self, channel, duration):

        endtime = datetime.now() + timedelta(seconds=duration*60)
        print("create token valid until {0}".format(endtime))

        file = open('/var/lock/heizung_token.txt', 'w')
        file.write('%d,%s\n'% (channel, endtime.strftime("%Y,%m,%d,%H,%M,%S") ) )
        file.flush()
        file.close()

    def heizung_all_off(self):
        # This requires a small patch in pifacedigitalio/core.py:
        ## else:
        ##    # finish configuring the board
        ##    #self.gpioa.value = 0
        ##    self.iodira.value = 0  # GPIOA as outputs
        # So the self.gpioa.value should not be set.
        if (self.pfd.output_port.value & 0x0f) is not 0x0f:
            self.pfd.output_pins[0].value=1 # "Schlafzimmer" (Buero)
            self.pfd.output_pins[1].value=1 # "Kinderzimmer" (Schlafzimmer)
            self.pfd.output_pins[2].value=1 # Bad
            self.pfd.output_pins[3].value=1 # Wohnzimmer
        sleep(0.1)
        print("State of Piface: {:08b} ".format(self.pfd.output_port.value))

    def heizung_1ch_on(self, channel):
        # TODO: Only one channel could be enabled at a time.
        self.heizung_all_off()
        self.pfd.output_pins[channel].value=0
        print("State of Piface: {:08b} ".format(self.pfd.output_port.value))

    def heizung_1ch(self, channel, duration):
        self.heizung_create_token(channel, duration)
        self.heizung_1ch_on(channel)
        self.add_off_event(datetime.now(), channel, duration)




