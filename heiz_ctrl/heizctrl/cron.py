#!/usr/bin/python

from time import sleep, strftime
from datetime import datetime, timedelta

from crontab import CronTab

class HeizungCronControl(object):
    def __init__(self):
        self.reload_crontab()

    def reload_crontab(self):
        self.crontab=CronTab(user=True)

    def list_events(self):
        self.reload_crontab()
        output = u'Events in Crontab\n'
        output += u'ID: Min Ho Day Mon DoW calling script\n'
        for i in range(len(self.crontab)):
            line = self.crontab[i]
            if line != "":
                output += ('%d: ' % i)  + (str(line) + '\n')
        return output

    # TODO: this function currently accepts only the line-number of the crontab
    def del_event(self,num):
        self.reload_crontab()
        print type(self.crontab[num])
        self.crontab.remove(self.crontab[num])
        self.crontab.write()
        return self.list_events()

    # TODO: this function clears all events in the crontab, not only ours. 
    def clear_all_events(self):
        self.reload_crontab()
        self.crontab.remove_all()
        self.crontab.write()

    def add_on_event(self, timestamp, channel, duration):
        self.reload_crontab()
        now = datetime.now()
        on_cmd = '/usr/local/bin/heizung_1ch_on.py -c {0} -t {1} -l /var/log/heiz_ctrl.log'.format(channel,duration)
        on_job = self.crontab.new(command=on_cmd)
        on_job.set_comment(timestamp.strftime('%Y.%m.%d %H:%M:%S,') + 'Heizung On')
        on_str = timestamp.strftime('%M %H %d %m *')
        on_job.setall(on_str)
        self.crontab.write()

    def add_off_event(self, timestamp, channel, duration):
        self.reload_crontab()
        now = datetime.now()
        off_job = self.crontab.new(command='/usr/local/bin/heizung_all_off.py -l /var/log/heiz_ctrl.log')
        off_job.set_comment(timestamp.strftime('%Y.%m.%d %H:%M:%S,') + 'Heizung Off')
        off_time = timestamp + timedelta(seconds=duration*60)
        off_str = off_time.strftime('%M %H %d %m *')
        off_job.setall(off_str)
        self.crontab.write()

    def add_single_event(self, timestamp, channel, duration):
        self.add_on_event(timestamp, channel, duration)
        self.add_off_event(timestamp, channel, duration)




