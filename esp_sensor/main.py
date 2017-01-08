# Temperature / Other sensor for ESP8266 board. 
# 
# Todolist:
# - Data storage while (deep) sleep


import time
import machine
import socket
import gc
import machine

import micropython

# micropython.alloc_emergency_exception_buf(100)
# Allocate RAM for exception buffer in interrupts

from wlan import mywlan
from machine import Pin
from machine import I2C

data_queue = False

board_id = '1'

class temperaturedata(object):
    def __init__(self):
        self.temp1 = -254.0
        self.temp2 = -254.0
        self.temp3 = -254.0
        self.timestamp = 0

    def dump(self):
        return board_id + ',' + str(self.timestamp) + ',' + str(self.temp1) + ','  + str(self.temp2) + ',' + str(self.temp3)


i2c0 = I2C(scl=Pin(2), sda=Pin(4), freq=10000)
# Sensor at 0x1b
i2c1 = I2C(scl=Pin(13), sda=Pin(12), freq=10000)
# Sensor at 0x1d
# i2c2 = I2C(scl=Pin(15), sda=Pin(14), freq=10000)
# Sensor not connected


def get_sensor():
    tdata = temperaturedata()

    tdata.timestamp = time.time()
    #tdata.temp1 = 1.0
    
    try:
        i2c0.writeto(0x1b, b'\x05')
        regs = i2c0.readfrom(0x1b, 2)
    except OSError:
        tdata.temp1 = -254.0
    else:
        tdata.temp1 = ((regs[0] & 0x0f) * 0x100  + (regs[1] & 0xff)) / 0x10


        if tdata.temp1 > 60.0 or tdata.temp1 < -10.0:
            tdata.temp1 = -254.0
    
    try:
        i2c1.writeto(0x1d, b'\x05')
        regs = i2c1.readfrom(0x1d, 2)
    except OSError:
        tdata.temp2 = -254.0
    else:
        tdata.temp2 = ((regs[0] & 0x0f) * 0x100  + (regs[1] & 0xff)) / 0x10

        if tdata.temp2 > 60.0 or tdata.temp2 < -10.0:
            tdata.temp2 = -254.0

    tdata.temp3 = -254.0

    return(tdata)

def take_temp_cb(timer):
    global data_queue

    if data_queue and len(data_queue.split(',')) > 200:
        print("Stopping measurements, risk of memory overflow")
        stop_temp()
        return

    #If more queue filled up, do not read samples
    if data_queue and len(data_queue.split(',')) > 120:
        print("Queue filled up, skipping measurement")
        pass
    else:

        tdata = get_sensor()

        if data_queue:
            data_queue += ',' + tdata.dump()
        else:
            data_queue = tdata.dump()

    print("Dataqueue: {0}".format(len(data_queue.split(',') )) )


tim = machine.Timer(-1)

def start_temp():
    tim.init(period=30000, mode=machine.Timer.PERIODIC, callback=take_temp_cb)

def stop_temp():
    tim.deinit()


def send_data(data):
    try:
        s = socket.socket()
        s.settimeout(5)
        s.connect( ('192.168.100.12', 6666) )
        s.sendall(data)
        response = s.recv(20)
        s.close()
    except OSError as e:
        print("send_data(): Socket OS error({0})".format(e))
        return b'0,error'

    return response
    #response could be "6,sleep", "0,nosleep" etc.


def send_data_loop():

    global data_queue
    errorcount = 0

    while(True):
        # Wait until first data is in queue:
        while(data_queue == False):
            pass
    
        wl.connect()
        # TODO: Seems to be a size limit, server receives only 80 words
        response = (send_data(data_queue)).decode()
        print("Got from Server: " + response)

        if int(response.split(',')[0]) is not len(data_queue.split(',')):
            # Server did not receive all data, try again after some delay.
            print('Response of server does not match queue length')
            errorcount += 1
            print('Errorcount {0}, Queue {1}'.format(errorcount, len(data_queue.split(','))) )
            # time.sleep(15 * errorcount)
        else:
            # all ok, clear queue
            data_queue = False
            print('Dataqueue: 0')
            errorcount = 0
            gc.collect()

        if errorcount > 5:
            break

        if response.split(',')[1] == 'deepsleep':
            # This is just for testing. Does not help a lot, since when deep-sleeping
            # also no data is taken from the sensor.
            print('Going to deep sleep')
            do_deepsleep(15)
            wl.off()
        if response.split(',')[1] == 'stop':
            # Stop this loop
            break
        elif response.split(',')[1] == 'nosleep':
            time.sleep(5*60)
        else:
            wl.off()
            time.sleep(5*60)


def do_deepsleep(seconds):
    rtc = machine.RTC()
    # Sleep n ms
    rtc.alarm(rtc.ALARM0, seconds * 1000)
    machine.deepsleep()
    # Deep sleep will return as reboot of the ESP



if __name__ == "__main__":
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # check if the device woke from a deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        machine_wakeup=1
    else:
        machine_wakeup=0

    start_temp()

    wl = mywlan()

    # Connect one time to trigger time sync
    wl.connect()
    wl.off()

    send_data_loop()

    stop_temp()
