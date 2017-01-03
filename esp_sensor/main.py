# Temperature / Other sensor for ESP8266 board. 
# 
# Todolist:
# - better iteration time handling
# - Wifi on/off on demand
# - Read multiple values, send once
# - Implement I2C sensors
# - Data storage while (deep) sleep


import time
import machine
import socket
import gc
import machine

from wlan import mywlan

data_queue = False

class temperaturedata(object):
    def __init__(self):
        self.temp1 = -254.0
        self.temp2 = -254.0
        self.temp3 = -254.0
        self.timestamp = 0

    def dump(self):
        return str(self.timestamp) + ',' + str(self.temp1) + ','  + str(self.temp2) + ',' + str(self.temp3) + ',||||,'


def get_temp():
    tdata = temperaturedata()
    
    tdata.timestamp = time.time()
    tdata.temp1 = 1.0
    tdata.temp2 = 2.0
    tdata.temp3 = 3.0
    
    return(tdata)


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
        return 'nok,stop'

    return response
    #response could be "ok,sleep", "nok,nosleep" etc.



def read_temp_loop():

    global data_queue

    while(True):
        tdata = get_temp()
        
        if data_queue:
            data_queue += tdata.dump()
        else:
            data_queue = tdata.dump()
        print(len(data_queue.split(',')))

        response = (send_data(data_queue)).decode()
        print(response)

        if int(response.split(',')[0]) is not len(data_queue.split(',')):
            break
        if response.split(',')[1] == 'deepsleep':
            print('Going to deep sleep')
            do_deepsleep()
        if response.split(',')[1] == 'stop':
            break
        else:
            time.sleep(9.99)
            gc.collect()


def do_deepsleep():
    rtc = machine.RTC()
    # Sleep n ms
    rtc.alarm(rtc.ALARM0, 5000)
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

    wl = mywlan()
    
    wl.connect()

    read_temp_loop()


