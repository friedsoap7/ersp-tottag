#!/usr/bin/env python3

# Import plotting library
#
# You may need to run "pip3 install matplotlib" in your terminal first
#
#   $ python3 quick_plot.py
#   Traceback (most recent call last):
#     File "/Users/ppannuto/Downloads/quick_plot.py", line 4, in <module>
#       import matplotlib.pyplot as plt
#   ModuleNotFoundError: No module named 'matplotlib'
#
# Fix with:
#
#   $ pip3 install matplotlib
#
import matplotlib.pyplot as plt

# Create a data structure to hold the parsed data
tags = {}

# Open the log file
f = open('03@11-05.log')

# Read data from the log file
for line in f:
    # For now, just ignore these events
    if line[0] == '#':
        continue

    # Parse out the fields
    timestamp,tag_id,distance = line.split()

    # Convert to meaningful data types
    timestamp = int(timestamp)
    tag_id = tag_id.split(':')[-1]
    distance = distance

    # Filter out bad readings
    if distance == 0 or distance == 999999:
        continue

    # Save this measurement
    if tag_id not in tags:
        tags[tag_id] = []
    tags[tag_id].append((timestamp, distance))

# Done parsing, plot!
for tag, data in tags.items():
    print("Plotting data for", tag)
    x_axis, y_axis = zip(*data)
    print(x_axis)
    print(y_axis)
    plt.plot(x_axis, y_axis)
    plt.show()
