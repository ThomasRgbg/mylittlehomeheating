# mylittlehomeheating

## Warning

Use at your own risk. There is no guarantee this works. 

## Limitations

The setup is currently hardcoded. E.g. there are currently 4 valves and 3 + 3 temperature channeles implemented. Making all of this
flexible would make the software much more complex and unreliable, so I keep it simple for the moment.

## Description

Some scripts, which are using an Raspberry PI with a PiFace digital like hardware interface. The scrips could enable the 
output of the IO-card for a certain amount of time.  The outputs are connected to relais, the relais control the motors of 
the heating channel valves. So currently a pure on/off operation. 

Some more scripts are used to read the temperatures and plot some nice graphs about it. Temperature is read by I2S based sensors. 
(Which are meanwhile cheaper and easier to adapt than a analog NTC or PT100 sensor)

Special features are: Remote control interface via XMPP, control daemon which checks for invalid software events to prevent a 
hang with heating enabled. 

### General idea

Instead of having a daemon running all the time triggering on/off events, a on-event is directly called. And for the corressponding off-event, an one-time entry in the user crontab is created. So the system cron takes care of switching something off again. 
To avoid any forgotten events, a hourly cronjobs checks additionally for forgotten events. 

## Todo/Ideas:

* Use the temperature to enable the heating in a room. Currently all ist just time based.
* Some more intelligent regulation of the time the heating is enabled. I have a very inert/slow underfloor heating. So when 
the temperature in the room rises, it is already to late to switch off the valve again. Instead the reflow pipe need to be
monitored in combination of the room temperature. 
* Use of remote temperature sensors. 
 * Tried already Bluetooth LowEnergy, which sucks on the software side.
 * I don't like proprietary stuff.
 * Currently playing with a ESP8266 based board and I2C based sensors. But running on battery might get a challenge.
* Nicer Webinterface with more statistic.
* Currently the fail-safe daemon allows only one channel enabled at one time. 

