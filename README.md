# brick-windows
code and configs for radio temperature sensors

I suppose someday I'll need more config info here, but for now, buildGraphs should be called by cron every 5 minutes or whatever
You should build a service file and enable it for radio_rfm69.py.

the .ino file goes on the feather M0 - you need to give each sensor a number.

The receiver is number 1, so you can have up to 8 sensors per receiver.

Could increase this, but you'd need to change the way packets are addressed.

Currently there's just one byte for sender, one for receiver.

**Hardware**
MCP9808 temp sensor: https://learn.adafruit.com/adafruit-mcp9808-precision-i2c-temperature-sensor-guide/arduino-code
- nothing special about this, just had it laying around

Adafruit Feather M0 Radio RFM69 915MHz: https://learn.adafruit.com/adafruit-feather-m0-radio-with-rfm69-packet-radio
- not the LoRa ones, and not the 433MHz ones.

Raspberry Pi Zero W
- this is great for 5-10 sensors and basic graphs. More sensors will mean more collectors.

Adafruit Radio Bonnet RFM69 915MHz: https://learn.adafruit.com/adafruit-radio-bonnets/overview
- the receiver side of the connection, this will mount on the raspberry pi

