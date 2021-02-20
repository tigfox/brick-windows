#!/usr/bin/env python3

# Import Python System Libraries
import time
from random import randint
import os

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
 
# 128x32 OLED Display
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
rfm69.node = 1
prev_packet = None
# Optionally set an encryption key (16 byte AES key). MUST match both
# on the transmitter and receiver (or be set to None to disable/the default).
rfm69.encryption_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x01\x02\x03\x04\x05\x06\x07\x08'

# Configure rrdtool database
# rrdtool.create("test.rrd", "--start", "now", "--step", "30", "RRA:AVERAGE:0.5:1:2880", "DS:2:GAUGE:60:0:100")

# Set some constants for config
storageDir = "/mnt/datadisk/temps/"

def storeReading(packet):
    sender = packet[1]
    data = packet[4:]
    outputFile = str(storageDir + str(sender) + "/" + str(sender) + ".temps")
    lockFile = str(storageDir +  str(sender) + "/" + str(sender) + ".lock")
    rrdfile = str(storageDir + str(sender) + "/" + str(sender) + ".rrd")
    if os.path.exists(str(storageDir + str(sender) + "/")): # make sure the output directory exists - what do if no?
        # print("output file: " + outputFile + " exists.")
        if os.path.exists(lockFile): # make sure the output file isn't being consumed by cron
            print("lock file exists, waiting")
            sleepTime = randint(1,500) / 1000
            print("sleeping to retry: " + str(sleepTime) + " seconds.")
            time.sleep(sleepTime) # if it is, wait
            storeReading(packet) # and then retry
        else: # data file exists, no lock file
            f = open(outputFile, "a+")
            # print("opened " + outputFile + " for writing")
            try:
                f.write(str(data.decode()) + "\n")
            except UnicodeDecodeError as e:
                print("Got a wonky packet: " + str(a))
            f.close()
            # print("closed " + outputFile)
    else:
        print("We have no output file. Weird packet? Should be: " + outputFile)
    try:
        rrdtool.update(rrdfile, "N:" + str(float(packet[4:])))
    except rrdtool.OperationalError as e:
        print("rrd db doesn't exist for sensor " + str(sender) + ". Creating new db at " + rrdfile)
        rrdtool.create(rrdfile, "--start", "now", "--step", "30", "RRA:AVERAGE:0.5:1:2880", "DS:" + str(sender) + ":GAUGE:60:0:100")
    except ValueError as e:
        print("rrd db couldn't update: " + str(e))
    return True

while True:
    packet = None
    # draw a box to clear the image
    display.fill(0)
    display.text('RasPi Radio', 35, 0, 1)
 
    # check for packet rx
    packet = rfm69.receive(with_ack=True, with_header=True)
    if packet is None:
        display.show()
        display.text('- Waiting for PKT -', 15, 20, 1)
    else:
        # Display the packet text and rssi
        display.fill(0)
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
