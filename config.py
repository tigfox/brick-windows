#!/usr/bin/env python3

# not actually using any of these yet, but we should be!

data_dir="/mnt/datadisk/"

radio_freq=915.00

# Reporting config

rrdCollector = True #simple rrd database, static graphs. great for small collectors, few sensors.
influxCollector = False #write to influxdb, either on a large collector or a remote db. fancy.

# how to handle sensor config? If we want different types of graphs for different types of sensors, we'll need a way to ID them better than just "number 1"

#radio1 = collector(1)
#radio2 = temp_sensor(2)
#radio3 = temp_sensor(3)
#radio4 = barometric(4)
#radio5 = liquid_sensor(5)


#def collector(radio_id):
#   pull settings (frequency, ID, rrd output file, etc) and return a collector object?

#def temp_sensor(radio_id):
#   same kind of thing for collector, but for any temp sensor

#def barometric(radio_id):
#   you're getting the idea now

#def liquid_sensor(radio_id):
#   I guess this is where we put the 
