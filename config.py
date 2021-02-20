#!/usr/bin/env python3
# Imports

# Radio hardware bits
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm69

# Storage
from influxdb import InfluxDBClient
data_dir="/mnt/datadisk/"

radio_freq=915.00

rrdCollector = False #simple rrd database, static graphs. great for small collectors, few sensors.
storage_path = str(data_dir + "rrd/"
rrd_file = "rrdfile.rrd"


influxCollector = True #write to influxdb, either on a large collector or a remote db. fancy.
influx_host = 'localhost'
influx_port = 8086
influx_user = 'collector'
influx_pass = '12 SPACE dicks'
influx_db = 'lrgcollector'


class Storage:
    def __init__(self):
        if influxCollector:
            self.name = influx_db
            self.client = InfluxDBClient(influx_host, influx_port, influx_user, influx_pass, influx_db)
        if rrdCollector:
            self.name = rrd_file    

    def write_data(self, entry):
        if influxCollector:
            client.write_points(entry)       
            client.close()
            # <fix> return status code here?
        if rrdCollector:
            try:
                rrdtool.update(rrdfile, "N:" + str(float(packet[4:])))
            except rrdtool.OperationalError as e:
                print("rrd db doesn't exist for sensor " + str(sender))

 
class Sensor:
    def __init__(self, node_num, sensor_type, location, adjustment=0):
        self.name = str("sensor" + str(node_num))
        self.type = sensor_type
        self.location = location
    def process_packet(self, packet):
        try:
            reading = packet[4:]
            adjusted = reading + adjustment
        except UnicodeDecodeError as e:
            print("funky packet, can't decode: " + str(e))
            return
        data = [{ "measurement" : self.type,
            "tags" : { 
                "sensor" : self.name,
                "location" : self.location
            }, 
            "fields" : { self.type : float(adjusted) }}]
        return data

radio1 = Collector(1)
radio2 = Sensor(2, "temperature", "Office")
radio3 = Sensor(3, "temperature", "Front Room")
#radio4 = Sensor(4, "barometric", "Office", -2)


