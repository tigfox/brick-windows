
How to build the collector

Download the most recent 'lite' version of raspian from the raspberry pi foundation
- Flash your card, get it on the wifi, etc.
- Follow the instructions here for circuitpython setup: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- Setup specific to the RFM69 radio: https://learn.adafruit.com/adafruit-radio-bonnets/rfm69-raspberry-pi-setup
- Git clone this repo

Set up the external drive: https://www.raspberrypi.org/documentation/configuration/external-storage.md
- Make it exfat, mount point should be /mnt/datadisk

InfluxDB Install
- Make sure to keep the db on the external drive so you don't wear out your SD card.
- Follow these instructions: https://pimylifeup.com/raspberry-pi-influxdb/

Grafana Install
- https://pimylifeup.com/raspberry-pi-grafana/

Put the Influx in the Grafana
- https://pimylifeup.com/raspberry-pi-internet-speed-monitor/
