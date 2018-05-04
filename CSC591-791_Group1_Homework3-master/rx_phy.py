import serial
import time
import collections
import threading
import socket
import sys


def sendDataOverSocket(data):
    global sk
    print 'Sending Data'
    sk.sendall(data)

def decodeFecFunction():
    global manchesterOutput
    global fecOutput
    global FEC_FACTOR

    if len(manchesterOutput)%FEC_FACTOR != 0:
        fecOutput.clear()
        # send 'FAIL'
        sendDataOverSocket('01000110010000010100100101001100')
        return
    else:
        while len(manchesterOutput) != 0:
            val = 0
            for x in range(FEC_FACTOR):
                val += manchesterOutput.popleft()
            
            if val >= FEC_FACTOR/2 + 1:
                fecOutput.append(1)
            else:
                fecOutput.append(0)
        
        #print fecOutput
        
        # Construct binary string from fecOutput buffer
        binString = ''
        lenPacket = len(fecOutput)
        for x in range(lenPacket):
            binString += str(fecOutput.popleft())
        print binString
        if binString[0:8] == '00000000' and binString[len(binString)-8:len(binString)] == '11111111':
            sendDataOverSocket(binString)
        else:
            # End or beginning not detected, send FAIL in binary
            sendDataOverSocket('01000110010000010100100101001100')

def decodeManchesterFunction():
    global parseBitsOutput
    global manchesterOutput

    # Error: Check if buffer length is not a multiple of 2
    if len(parseBitsOutput)%2 != 0:
        return
    else:
        while len(parseBitsOutput) != 0:
            bit0 = parseBitsOutput.popleft()
            bit1 = parseBitsOutput.popleft()

            # Decode as 0 if 1 -> 0
            if bit0 == 1 and bit1 == 0:
                manchesterOutput.append(0)
            
            # Decode as 1 if 0 -> 1
            if bit0 == 0 and bit1 == 1:
                manchesterOutput.append(1)

    print manchesterOutput
    decodeFecFunction()

def parseBitsFunction():
    
    global bufferWindow
    global parseBitsOutput

    count_1 = 0
    count_0 = 0
    prevBit = 0

    while len(bufferWindow) != 0:
        bit = bufferWindow.popleft()

        # Check for blocks of size 4 or more when bit stream toggles (0 -> 1 or 1 -> 0)
        if count_0 + count_1 > 3 and bit != prevBit:
            if count_0 > count_1:
                parseBitsOutput.append(0)
                if count_0 > 8: # Double zeros if block size is more than 8
                    parseBitsOutput.append(0)
            else:
                parseBitsOutput.append(1)
                if count_1 > 7: # double ones if block size is more than 7
                    parseBitsOutput.append(1)
            
            # Reset count vars for counting next block size
            count_1 = 0
            count_0 = 0

        # Increment respective bit counter for each block
        if bit == 1:
            count_1 += 1
        elif bit == 0:
            count_0 += 1

        prevBit = bit    
            
        
    # End Tx when continuous samples of zero observed and start decoding    
    if count_0 + count_1 > 28 and count_0 > 28 and len(parseBitsOutput)%2 == 1:
        parseBitsOutput.append(0)
    print parseBitsOutput
    bufferWindow = collections.deque([])
    decodeManchesterFunction()


ser = serial.Serial('/dev/cu.usbmodem1411',2000000)


HOST = '127.0.0.1'
PORT = int(sys.argv[1])

sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sk.connect((HOST,PORT))

# Global parameters
WINDOWSIZE = 30
WINDOWPEAK = 3
FEC_FACTOR = 1
startTx = False
THRESHOLD = 600

# Buffers for parsing and decoding bits
window = collections.deque([], maxlen=WINDOWSIZE)
windowPeak = collections.deque([], maxlen=WINDOWPEAK)
bufferWindow = collections.deque([])
parseBitsOutput = collections.deque([])
manchesterOutput = collections.deque([])
fecOutput = collections.deque([])

#DEBUG
outputList = []
initTime = time.time()
counter = 0
sliceLength = 0

#start looping to receive ADC values
try:
    while ser.isOpen():
        
        #get continuous values
        value = ser.readline()
        value = value.strip()
        
        # Convert to integer type
        try:
            value = int(value)
        except:
            continue

        # Compare with THRESHOLD and decide if value is 1 or 0
        if value > THRESHOLD:
            value = 1
        else:
            value = 0
        
        window.append(value)
        windowPeak.append(value)
        if startTx == True:
            bufferWindow.append(value)

        # If peak detected, set startTx flag
        if sum(windowPeak) == 3 and startTx == False:
            startTx = True
            for x in range(3):
                bufferWindow.append(windowPeak[x])
        
        # If continuous zeros found, tx ends
        elif sum(window) == 0:
            startTx = False
            if len(bufferWindow) != 0:
                parseBitsFunction()
        
        # DEBUG CODE
        counter += 1
        # if time.time()-initTime > 10:
        #     break

except Exception as inst:
    print type(inst)
    print inst.args
    print inst
    sliceLength = counter/(time.time()-initTime)
    print sliceLength
    ser.close()
    #fh = open('output','w')
    #fh.write('\n'.join(map(str,outputList)))

    print 'Exception'
