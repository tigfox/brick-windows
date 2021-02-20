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

#simple rrd database, static graphs. great for small collectors, few sensors.
rrdCollector = False
storage_path = str(data_dir + "rrd/")
rrd_file = "rrdfile.rrd"

#write to influxdb, either on a large collector or a remote db. fancy.
influxCollector = True
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

class Collector:
    def __init__(self, node_number):
        # Button A
        btnA = DigitalInOut(board.D5)
        btnA.direction = Direction.INPUT
        btnA.pull = Pull.UP
         
        # Button B
        btnB = DigitalInOut(board.D6)
        btnB.direction = Direction.INPUT
        btnB.pull = Pull.UP
         
        # Button C
        btnC = DigitalInOut(board.D12)
        btnC.direction = Direction.INPUT
        btnC.pull = Pull.UP
         
        # Create the I2C interface.
        i2c = busio.I2C(board.SCL, board.SDA)
         
        # 128x32 built-in OLED Display
        reset_pin = DigitalInOut(board.D4)
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
        # Clear the display.
        display.fill(0)
        display.show()
        width = display.width
        height = display.height
         
        # Configure Packet Radio
        CS = DigitalInOut(board.CE1)
        RESET = DigitalInOut(board.D25)
        spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        rfm69 = adafruit_rfm69.RFM69(spi, CS, RESET, 915.0)
        rfm69.node = node_number
        prev_packet = None
        # Optionally set an encryption key (16 byte AES key). MUST match both
        # on the transmitter and receiver (or be set to None to disable/the default).
        rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'


radio1 = Collector(1)
radio2 = Sensor(2, "temperature", "Office")
radio3 = Sensor(3, "temperature", "Front Room")
#radio4 = Sensor(4, "barometric", "Office", -2)


