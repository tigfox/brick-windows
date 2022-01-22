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
influx_pass = '12 SPACE ducks'
influx_db = 'lrgcollector'

target_temp = 22

class Boiler:
    def __init__(self):
        self.running = False

    def get_status(self):
        #send getStatus packet
        #await returned status
        pass

    def turn_on(self):
        self.running = True
        #send turn on command

    def turn_off(self):
        self.running = False
        #send turn off command

class Storage:
    def __init__(self):
        if influxCollector:
            self.name = influx_db
            self.client = InfluxDBClient(influx_host, influx_port, influx_user, influx_pass, influx_db)
        if rrdCollector:
            self.name = rrd_file

    def write_data(self, entry):
        if influxCollector:
            self.client.write_points(entry)
            self.client.close()
            # <fix> return status code here?
        if rrdCollector:
            try:
                rrdtool.update(rrdfile, "N:" + str(float(packet[4:])))
            except rrdtool.OperationalError as e:
                print("rrd db doesn't exist for sensor " + str(sender))


class Sensor:
    def __init__(self, node_num, location, sensor_list, adjustment=0):
        '''
        node_num = radio node number
        location = string
        sensor_list = [{ "type" : "Temperature", "packet_key" : "T", "adjustment" : 0}, { "type" : "CO2", "packet_key" : "C", "adjustment" : 0}]
        '''
        self.name = str("sensor" + str(node_num))
        self.sensor_list = sensor_list
        self.location = location

    def process_packet(self, packet):
        try:
            split_pkt = []
            split_pkt = packet.split(b':')
            # print(dags)
            node_num = int(split_pkt[1].decode())
            pkt_key = str(split_pkt[2].decode())
            reading = float(split_pkt[3].decode())
            sentype = next((sentype['type'] for sentype in self.sensor_list if sentype['packet_key'] == pkt_key), None)
            # print("sensor type from reading: " + sentype)
            adjusted = reading + next((sentype['adjustment'] for sentype in self.sensor_list if sentype['packet_key'] == pkt_key), None)
        except UnicodeDecodeError as e:
            print("funky packet, can't decode: " + str(e))
            return None
        data = [{ "measurement" : sentype,
            "tags" : {
                "sensor" : self.name,
                "location" : self.location
            },
            "fields" : { sentype : float(adjusted) }}]

        return data

class Collector:
    def __init__(self, node_number):
        self.node_number = node_number

        # Button A
        self.btnA = DigitalInOut(board.D5)
        self.btnA.direction = Direction.INPUT
        self.btnA.pull = Pull.UP

        # Button B
        self.btnB = DigitalInOut(board.D6)
        self.btnB.direction = Direction.INPUT
        self.btnB.pull = Pull.UP

        # Button C
        self.btnC = DigitalInOut(board.D12)
        self.btnC.direction = Direction.INPUT
        self.btnC.pull = Pull.UP

        # Create the I2C interface.
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # 128x32 built-in OLED Display
        self.reset_pin = DigitalInOut(board.D4)
        self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c, reset=self.reset_pin)
        # Clear the display.
        self.display.fill(0)
        self.display.show()
        self.width = self.display.width
        self.height = self.display.height

        # Configure Packet Radio
        self.CS = DigitalInOut(board.CE1)
        self.RESET = DigitalInOut(board.D25)
        self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self.rfm69 = adafruit_rfm69.RFM69(self.spi, self.CS, self.RESET, radio_freq)
        self.rfm69.node = node_number
        self.prev_packet = None
        # Optionally set an encryption key (16 byte AES key). MUST match both
        # on the transmitter and receiver (or be set to None to disable/the default).
        self.rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'


# radio1 = Collector(1)
# radio2 = Sensor(2, "temperature", "Office")
# radio3 = Sensor(3, "temperature", "Front Room")
#radio4 = Sensor(4, "barometric", "Office", -2)


