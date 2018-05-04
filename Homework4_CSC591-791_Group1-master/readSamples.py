import serial
import collections


count = 10

BUFFERLEN = 800
sampleArray = collections.deque([],maxlen=BUFFERLEN)
meanArray = collections.deque([],maxlen=150)
sampleVal = None

# open serial port and continuously read IMU values

# serPort = serial.Serial("/dev/tty/ACM0")
serPort = serial.Serial("/dev/cu.usbmodem1421",2000000)

if(serPort.isOpen()):
    val = serPort.readline()
    val = val.strip()
    count += 1

    if val == "Begin":
        count = -1

    # Record only thegyro-y values as they have maximum variance
    if count == 4:
        sampleVal = float(val)

    # Fill a pipe with the IMU values
    if val == "End":
    	if sampleVal != None:
        	sampleArray.append(sampleVal)
        	meanArray.append(sampleVal)
	
	# If value higher than 7 found, set high value flag to true
	if abs(sampleVal) > 7:
		previousHigh = True

    # if tail detected i.e. continuous low values then empty the buffer and send the samples for detection
    # can replace moving average with exponential average, but what should be the weight?
    if float(sum(meanArray))/len(meanArray) < 3 and previousHigh = True:
    	previousHigh = False
    	
    	# code for sending samples to bluemix
    	# STUB CODE
    	
    	# empty buffer and start collecting fresh set of samples
    	sampleArray = collections.deque([],maxlen=BUFFERLEN)
	

