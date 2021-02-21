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
# Set some constants for config
# storageDir = "/mnt/datadisk/temps/"

# def storeReading(packet):
#     sender = packet[1]
#     data = packet[4:]
#     outputFile = str(storageDir + str(sender) + "/" + str(sender) + ".temps")
#     lockFile = str(storageDir +  str(sender) + "/" + str(sender) + ".lock")
#     rrdfile = str(storageDir + str(sender) + "/" + str(sender) + ".rrd")
#     if os.path.exists(str(storageDir + str(sender) + "/")): # make sure the output directory exists - what do if no?
#         # print("output file: " + outputFile + " exists.")
#         if os.path.exists(lockFile): # make sure the output file isn't being consumed by cron
#             print("lock file exists, waiting")
#             sleepTime = randint(1,500) / 1000
#             print("sleeping to retry: " + str(sleepTime) + " seconds.")
#             time.sleep(sleepTime) # if it is, wait
#             storeReading(packet) # and then retry
#         else: # data file exists, no lock file
#             f = open(outputFile, "a+")
#             # print("opened " + outputFile + " for writing")
#             try:
#                 f.write(str(data.decode()) + "\n")
#             except UnicodeDecodeError as e:
#                 print("Got a wonky packet: " + str(a))
#             f.close()
#             # print("closed " + outputFile)
#     else:
#         print("We have no output file. Weird packet? Should be: " + outputFile)
#     try:
#         rrdtool.update(rrdfile, "N:" + str(float(packet[4:])))
#     except rrdtool.OperationalError as e:
#         print("rrd db doesn't exist for sensor " + str(sender) + ". Creating new db at " + rrdfile)
#         rrdtool.create(rrdfile, "--start", "now", "--step", "30", "RRA:AVERAGE:0.5:1:2880", "DS:" + str(sender) + ":GAUGE:60:0:100")
#     except ValueError as e:
#         print("rrd db couldn't update: " + str(e))
#     return True


collector = Collector(1)
radio2 = Sensor(2, "temperature", "Office")
radio3 = Sensor(3, "temperature", "Front Room")
#radio4 = Sensor(4, "barometric", "Office", -2)

while True:
    packet = None
    # draw a box to clear the image
    collector.display.fill(0)
    collector.display.text('Collector ' + str(collector.node_number), 35, 0, 1)
 
    # check for packet rx
    packet = rfm69.receive(with_ack=True, with_header=True)
    if packet is None:
        collector.display.show()
        collector.display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        collector.display.fill(0)
        if packet[0] == rfm69.node:
            try:
                prev_packet = packet
                storeReading(prev_packet)
                sender = prev_packet[1]
                packet_text = str(prev_packet[4:], "utf-8")
                display.text(str(sender) + ': ', 0, 0, 1)
                display.text(packet_text, 25, 0, 1)
                time.sleep(1)
            except UnicodeDecodeError as e:
                print("funky packet: " + str(e)) 

    if not btnA.value:
        # Send Button A
        display.fill(0)
        #button_a_data = bytes("Button A!\r\n","utf-8")
        # rfm69.send(button_a_data)
        display.text("That's Button A!", 25, 15, 1)
    elif not btnB.value:
        # Send Button B
        display.fill(0)
        #button_b_data = bytes("Button B!\r\n","utf-8")
        #rfm69.send(button_b_data)
        display.text("That's Button B!", 25, 15, 1)
    elif not btnC.value:
        # Send Button C
        display.fill(0)
        #button_c_data = bytes("Button C!\r\n","utf-8")
        #rfm69.send(button_c_data)
        display.text("That's Button C!", 25, 15, 1)
 
    display.show()
    time.sleep(0.1)
