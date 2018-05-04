import datetime
import time
import random
import matplotlib.pyplot as plt
import matplotlib.dates as md
import json
import collections
from dateutil.parser import parse
import numpy as np

with open('position.json') as file:
	positions = json.load(file)

positions = collections.OrderedDict(sorted(positions.items(), key=lambda x: parse(x[0])))

timestamps=[]
positionsList = []
for ts in positions:
	timestamps.append(ts)
	positionsList.append(positions[ts])

values=[]
for ts in positions:
	values.append(positions[ts])

x=[]
for t in timestamps:
	x.append(md.datestr2num(t))

y = []
for value in values:
	y.append(value)

strides=[]
for i in range(len(positionsList)-1):
	strides.append(positionsList[i+1]-positionsList[i])
strides.append(0)

plt.figure()
plt.gca().xaxis.set_major_formatter(md.DateFormatter("%M:%S.%f"))
plt.xticks(rotation=90)
plt.title("Position VS Time")
plt.ylabel("Position")
plt.xlabel("Time")
plt.plot(x, y,"o")
plt.plot(x, y)

plt.savefig(fname="../../../../../591project/pvapp_site/pvapp/static/images/position_data.png", dpi=65, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)


plt.figure()
plt.gca().xaxis.set_major_formatter(md.DateFormatter("%M:%S.%f"))
plt.xticks(rotation=90)
plt.title("Speed VS Time")
plt.ylabel("Speed")
plt.xlabel("Time")
plt.plot(x, np.gradient(y))

plt.savefig(fname="../../../../../591project/pvapp_site/pvapp/static/images/speed_data.png", dpi=65, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)


plt.figure()
plt.xticks(rotation=90)
plt.title("Stride Lengths")
plt.ylabel("Stride Length")
plt.xlabel("Stride Number")
plt.bar(range(len(strides)), strides)

plt.savefig(fname="../../../../../591project/pvapp_site/pvapp/static/images/stride_data.png", dpi=65, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)



#plt.show()

