# brick-windows
code and configs for radio temperature sensors

I suppose someday I'll need more config info here, but for now, buildGraphs should be called by cron every 5 minutes or whatever
You should build a service file and enable it for radio_rfm69.py
the .ino file goes on the feather M0 - you need to give each sensor a number.
The receiver is number 1, so you can have up to 8 sensors per receiver.
Could increase this, but you'd need to change the way packets are addressed.
Currently there's just one byte for sender, one for receiver.

