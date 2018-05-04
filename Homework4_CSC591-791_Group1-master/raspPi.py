import serial
import sys
import time
# serPort = serial.Serial("/dev/tty/ACM0")
serPort = serial.Serial("/dev/cu.usbmodem1421",2000000)

data = [0,0,0,0,0,0]


count = 10
timerVal = float(sys.argv[1])
print timerVal
label = str(sys.argv[2])
now = time.time()
fileArray = []
while time.time() - now < float(timerVal):
    if(serPort.isOpen()):
        val = serPort.readline()
        val = val.strip()
        count += 1

        if val == "Begin":
            count = -1

        if count in [0,1,2,3,4,5]:
            data[count] = float(val)

        if val == "End":
            print(data)
            fileArray.append(data)
            data = [0,0,0,0,0,0]

fh = open('{}_{}'.format(time.time(),label),'w')
for val in fileArray:
    fh.write(','.join(map(str,val)))
    fh.write('\n')
fh.close()
