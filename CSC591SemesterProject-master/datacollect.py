# Data collection module

import RPi.GPIO as GPIO
import time
import numpy as np
import sys
import socket
import os

# Declare all the constants here
	# Number of Pis
	# Number of sensors on each raspberry pi
	# pin numbers of each sensor pair
	# pin number of Pi connections
	# ip address of processing pi
PI_ID = int(sys.argv[1]) # 0 or 1
numPiLen = int(sys.argv[2]) # 2 for the purpose of demo
SENSE_PER_PI = int(sys.argv[3]) # 6 for the purpose of demo
DEBUG = bool(int(sys.argv[4])) # 0 for false, 1 for true
ALPHA = 1 # exponential average factor
STOP = False
SETTLE_DELAY = 0.5
IP_PROCESSOR = '192.168.43.99'
PORT = 5050
CONNECT_PI_OUT_PIN = 19
CONNECT_PI_IN_PIN = 21
FIRST_RUN = True
userName="anirudhganji"
PASS="123"
pathToFile="~/iotProject"
window = 10


# Create Pi ids
# default value : piId = [0,1]
piId = [] 
for x in range(numPiLen):
	piId.append(x)

# Create number of sensors per pi
# default value : sensors = [6,6]
sensors = [] 
# Create sensor ids
for x in range(numPiLen):
	sensors.append(SENSE_PER_PI)

# create mapppings to RPi pins
# default value : pinArray[sensorId][0:TRIG, 1:ECHO] = [ []..., ]
#pinArray = [ [3,5],[8,10],[11,13],[16,18],[22,24],[29,31] ] 
pinArray = [ [8,10],[22,24] ]

# Calibration array
calValues = []


# Initialize all GPIO pins to false
GPIO.setmode(GPIO.BOARD)

GPIO.setup(CONNECT_PI_IN_PIN,GPIO.IN)
GPIO.setup(CONNECT_PI_OUT_PIN,GPIO.OUT)
GPIO.output(CONNECT_PI_OUT_PIN,False)

for x in range(numPiLen):
	for y in range(sensors[x]):
		TRIG = pinArray[y][0]
		ECHO = pinArray[y][1]

		GPIO.setup(TRIG,GPIO.OUT)
		GPIO.setup(ECHO,GPIO.IN)

		GPIO.output(TRIG, False)
print 'Completed hardware initilization'
time.sleep(SETTLE_DELAY)


# calibrate sensors
for x in range(numPiLen):
	calValues.append([])
	for y in range(sensors[x]):
		calValues[x].append([])
		TRIG = pinArray[y][0]
		ECHO = pinArray[y][1]
		values = []
		for runs in range(10):
			# Send pulse
			GPIO.output(TRIG, True)
			time.sleep(0.00001)
			GPIO.output(TRIG, False)

			# Calculate RTT
			while GPIO.input(ECHO)==0:
				pulse_start = time.time()

			while GPIO.input(ECHO)==1:
				pulse_end = time.time()   

			# Calculate distance in cm
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration*17150
			distance = round(distance, 2)
			values.append(distance)
		calValues[x][y] = []
		calValues[x][y].append(np.mean(values))
		calValues[x][y].append(np.std(values))
print 'Completed calibration'

if DEBUG == True:
	for x in range(numPiLen):
		#print calValues[x]
		pass

######################## start data collection ################################

fh = open('output_{}'.format(PI_ID),'w')
now = time.time()



# Create value arrays for each sensor on this pi
sensorVal = []
for x in range(sensors[PI_ID]):
	sensorVal.append(0)


if DEBUG == True:
	count = 0

try:
	while time.time()-now < window:

		if numPiLen != 1:
			if PI_ID != 0:
				while GPIO.input(CONNECT_PI_IN_PIN) == 0:
					pass

		# get start time
		sample_start = time.time()

		# loop through sensors in this Pi
		for x in range(sensors[PI_ID]):
			TRIG = pinArray[x][0]
			ECHO = pinArray[x][1]

			# Send pulse
			GPIO.output(TRIG, True)
			time.sleep(0.00001)
			GPIO.output(TRIG, False)

			# Calculate RTT
			while GPIO.input(ECHO)==0:
				pulse_start = time.time()

			while GPIO.input(ECHO)==1:
				pulse_end = time.time()   

			# Calculate distance in cm
			pulse_duration = pulse_end - pulse_start
			distance = pulse_duration*17150
			distance = round(distance, 2)

			if sensorVal[x] == 0:
				sensorVal[x] = distance
			else:
				sensorVal[x] = ALPHA*distance + (1-ALPHA)*sensorVal[x]
			
		# get end time
		sample_end = time.time()


		if DEBUG == True:
			#print sensorVal
			count += 1
			if count > 30:
				STOP = True
		
		# After looping, publish start, end time and these values to the processor
		valStr = str(PI_ID) + ' '
		valStr += str(sample_start) + ' ' + str(sample_end)
		for x in range(len(sensorVal)):
			valStr += ' ' + str(sensorVal[x])
		
		if DEBUG == 1:
			print valStr

		#soc.send(valStr)
		fh.write(valStr)
		fh.write('\n')

		
		

		# Let the other Pi know that it can start collecting data
		GPIO.output(CONNECT_PI_OUT_PIN,True)
		#time.sleep()
		

		# wait for acknowledgement from other pi when its done collecting data
		if numPiLen != 1:
			print 'multiple'
			if PI_ID == 0:
				while GPIO.input(CONNECT_PI_IN_PIN) == 0:
					pass
			else:
				while GPIO.input(CONNECT_PI_IN_PIN) == 1:
					pass
			
			GPIO.output(CONNECT_PI_OUT_PIN,False)	
			
		if DEBUG == True:
			print 'Done one sample'
		
		if FIRST_RUN:
			now = time.time()

		# after first run, make it false
		FIRST_RUN = False
except:
	print 'Server Timed out'

fh.close()
GPIO.output(CONNECT_PI_OUT_PIN,False)
GPIO.cleanup()

cmd='sshpass -p "'+PASS+'" scp output_'+str(PI_ID)+' '+userName+'@'+str(IP_PROCESSOR)+':'+pathToFile
print cmd
os.system(cmd)
