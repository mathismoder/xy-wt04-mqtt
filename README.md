# xy-wt04-mqtt
Transmit data from xy-wt04 via MQTT

What you need: at the heart is the XY-WT04 thermocouple adaptor + a thermocouple sensor.
Add to this a Pi Pico W some lines of script to read the modbus registers (see http://myosuploads3.banggood.com/products/20220717/20220717212911XY-WT04-EN.pdf)
This get then transmitted via MQTT to the broker of your choice.

What took me a while was to find out the baudrate + address the module was talking at (115200).

So for probing (on linux) best try something like the following (connect RX/TX lines to a FTDI beforehand):

```
mbpoll -b 115200 -P none -a 2 -r 4 /dev/ttyUSB0
...
-- Polling slave 2... Ctrl-C to stop)
[4]:     252
``` 
In my case i had to change the modbus address (long pressing set, then advancing to the address, changing, long press saves).
