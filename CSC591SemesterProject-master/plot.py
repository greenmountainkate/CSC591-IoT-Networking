import datetime
import time
import random
import matplotlib.pyplot as plt
import matplotlib.dates as md
import json

import collections
from dateutil.parser import parse
import pandas as pd
import numpy as np

from scipy import interpolate
from numpy import arange
from numpy import sin,linspace,power
from pylab import plot,show

def draw_tangent(x,y,a):
 # interpolate the data with a spline
 spl = interpolate.splrep(x,y)
 small_t = arange(a-5,a+5)
 fa = interpolate.splev(a,spl,der=0)     # f(a)
 fprime = interpolate.splev(a,spl,der=1) # f'(a)
 tan = fa+fprime*(small_t-a) # tangent
 plot(a,fa,'om',small_t,tan,'--r')
 

with open('position.json') as file:
	positions = json.load(file)

positions = collections.OrderedDict(sorted(positions.items(), key=lambda x: parse(x[0])))

timestamps=[]
for ts in positions:
	timestamps.append(ts)

values=[]
for ts in positions:
	values.append(positions[ts])

x=[]
for t in timestamps:
	x.append(md.datestr2num(t))
y = []
for value in values:
	y.append(value)

xticks=[]
for i, v in enumerate(x):
	if i%2==0:
		xticks.append(v)


plt.gca().xaxis.set_major_formatter(md.DateFormatter("%M:%S.%f"))
plt.xticks(xticks)
plt.xticks(rotation=90)
plt.yticks(y)
plt.plot(x, y,"o")

# plot (x, y)
# for p in range(len(x)):
# 	draw_tangent(x,y,x[p])


# show()


plt.plot(x, y)
plt.title("Position VS Time")
plt.ylabel("Position")
plt.xlabel("Time")

plt.show()

