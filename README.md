# mylittlehomeheating

## Warning

Use at your own risk. There is no guarantee this works. 

## Description

Some scripts, which are using an Raspberry PI with a PiFace digital like hardware interface. The scrips could enable the 
output of the IO-card for a certain amount of time.  The outputs are connected to relais, the relais control the motors of 
the heating channel valves. So currently a pure on/off operation. 

Some more scripts are used to read the temperatures and plot some nice graphs about it. Temperature is read by I2S based sensors. 
(Which are meanwhile cheaper and easier to adapt than a analog NTC or PT100 sensor)

Special features are: Remote control interface via XMPP, control daemon which checks for invalid software events to prevent a 
hang with heating enabled. 

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

