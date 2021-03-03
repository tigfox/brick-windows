#!/usr/bin/env python3
 

"""
Example for using the RFM69HCW Radio with Raspberry Pi.
 
Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
Author: Brent Rubell for Adafruit Industries
Thanks Brent!
"""
# Import Python System Libraries
import time
from random import randint
import os

import config


storage = config.Storage()
collector = config.Collector(1)
radio2 = config.Sensor(2, "Outside", [{ "type" : "Temperature", "packet_key" : "T", "adjustment" : 0}])
radio3 = config.Sensor(3, "Front Room", [{ "type" : "Temperature", "packet_key" : "T", "adjustment" : 0}, { "type" : "CO2", "packet_key" : "C", "adjustment" : 0}])
radio4 = config.Sensor(4, "Office", [{ "type" : "Temperature", "packet_key" : "T", "adjustment" : 0}, { "type" : "CO2", "packet_key" : "C", "adjustment" : 0}])
radio5 = config.Sensor(5, "Bedroom", [{ "type" : "Temperature", "packet_key" : "T", "adjustment" : 0}, { "type" : "CO2", "packet_key" : "C", "adjustment" : 0}])
radio6 = config.Sensor(6, "Basement", [{ "type" : "Water", "packet_key" : "W", "adjustment" : 0}])

while True:
    packet = None
    # draw a box to clear the image
    collector.display.fill(0)
    collector.display.text('Collector ' + str(collector.node_number), 35, 0, 1)
 
    # check for packet rx
    packet = collector.rfm69.receive(with_ack=True, with_header=True)
    if packet is None:
        collector.display.show()
        collector.display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        collector.display.fill(0)
        pkt_data = []
        pkt_data = packet.split(b':')
        if packet[0] == collector.rfm69.node:
            try:
                node_num = int(pkt_data[1].decode())
                read_type = str(pkt_data[2].decode())
                reading = float(pkt_data[3].decode())
                # print("Sensor " + str(pkt_data[1].decode()) + " reporting a " + str(pkt_data[2].decode()) + " reading of " + str(pkt_data[3].decode()))
                prev_packet = packet
                if node_num == 2:
                    data_reading = radio2.process_packet(prev_packet)
                if node_num == 3:
                    data_reading = radio3.process_packet(prev_packet)
                if node_num == 4:
                    data_reading = radio4.process_packet(prev_packet)
                if node_num == 5:
                    data_reading = radio5.process_packet(prev_packet)
                if node_num == 6:
                    data_reading = radio6.process_packet(prev_packet)
                if data_reading is not None:
                    storage.write_data(data_reading)
                packet_text = str(prev_packet[4:], "utf-8")
                collector.display.text(str(node_num) + ': ', 0, 0, 1)
                collector.display.text(str(reading), 25, 0, 1)
                time.sleep(1)
            except UnicodeDecodeError as e:
                print("funky packet: " + str(e)) 
            except ValueError as e:
                print("funky packet: " + str(e))

    if not collector.btnA.value:
        # Send Button A
        collector.display.fill(0)
        #button_a_data = bytes("Button A!\r\n","utf-8")
        # rfm69.send(button_a_data)
        collector.display.text("That's Button A!", 25, 15, 1)
    elif not collector.btnB.value:
        # Send Button B
        collector.display.fill(0)
        #button_b_data = bytes("Button B!\r\n","utf-8")
        #rfm69.send(button_b_data)
        collector.display.text("That's Button B!", 25, 15, 1)
    elif not collector.btnC.value:
        # Send Button C
        collector.display.fill(0)
        #button_c_data = bytes("Button C!\r\n","utf-8")
        #rfm69.send(button_c_data)
        collector.display.text("That's Button C!", 25, 15, 1)
 
    collector.display.show()
    time.sleep(0.1)
