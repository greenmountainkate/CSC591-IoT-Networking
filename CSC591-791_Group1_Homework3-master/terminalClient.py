import socket
import sys
import binascii
import threading


packetBitSize=64 # Change this if you want to change packet size in bits.
packetByteSize=packetBitSize/8
sizedData=[]
binaryList=[]

startStr="0START"
doneTZ="0DONE"
doneTO="1DONE"
newSize=packetByteSize+1
doneZ=doneTZ.ljust(newSize)
doneO=doneTO.ljust(newSize)
starStr=startStr.ljust(newSize)
one="1"
zero="0"

def toBinary(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int(binascii.hexlify(text.encode(encoding, errors)), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def fromBinary(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return int2bytes(n).decode(encoding, errors)

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))

startBin=toBinary(starStr)
doneBin0=toBinary(doneZ)
doneBin1=toBinary(doneO)

def dataToPacket(plainData):
	# text smaller than packet
	if dataLen < packetByteSize:
		newData=one+plainData
		sizedData.append(newData.ljust(packetByteSize))

	# text same size as packet
	if dataLen == packetByteSize:
		newData=one+plainData
		sizedData.append(newData)

	# text bigger than packet
	if dataLen > packetByteSize:
		quotient=dataLen/packetByteSize
		if quotient*packetByteSize == dataLen:
			newQuotient=quotient
		else:
			newQuotient=quotient+1
		#For Adjusting Total Size
		multSize=(newQuotient)*packetByteSize
		extendedData=plainData.ljust(multSize)
		#For adding the correct pre-seq
		for i in range(0,newQuotient):
			if i%2 == 0:
				seqStr=one
			else:
				seqStr=zero
			toAdd=str(seqStr)+str(extendedData[i*packetByteSize:((i+1)*packetByteSize)])
			sizedData.append(toAdd)

	# Building the binary list
	listSize=len(sizedData)
	binaryList=[startBin]

	for i in range(0,listSize):
		binaryList.append(toBinary(sizedData[i]))

	binSize=len(binaryList)
	if binSize%2==0:
		binaryList.append(doneBin0)
	else:
		binaryList.append(doneBin1)

	return binaryList


if (len(sys.argv)==2):
	userInput=raw_input("Enter Input: ")
	dataLen=len(userInput)
	dataToTransmit = dataToPacket(userInput)
	for d in dataToTransmit:
		print d +"\n"

elif (len(sys.argv)==3):
	filePath = sys.argv[2]
	with open(filePath, 'r') as myFile:
		userInput = myFile.read()
		dataLen=len(userInput)
		dataToTransmit = dataToPacket(userInput)
		for d in dataToTransmit:
			print d +"\n"
else: sys.exit()






########################################################################################################
class messageSender(threading.Thread):
	def __init__(self, clientIP, clientPort, txData):
		threading.Thread.__init__(self)
		self.clientIP = clientIP
		self.clientPort = clientPort
		self.txData = txData

	def run(self):
		try:

			connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			connection.connect((self.clientIP, self.clientPort))
			connection.sendall("SEND")
			connection.recv(1024).decode()
			print str(len(self.txData))
			connection.sendall(str(len(self.txData)))
			connection.recv(1024).decode()
				
			for i in range(len(self.txData)):
				connection.sendall(self.txData[i])
				
				serverStatus = str(connection.recv(1024).decode())

				if (serverStatus=="BUSY"):
					connection.sendall("OK")
					print('-'*70)
					print("Server is [BUSY] sending chunk "+str(i+1)+" of "+str(len(self.txData)))
					print('-'*70)

				serverStatus = str(connection.recv(1024).decode())
				if (serverStatus=="AVAILABLE"):
					connection.sendall("OK")
					print ("Sent Chunk "+str(i+1) +" of "+str(len(self.txData)))
					print('-'*70)
					print("Server is [READY]")
					print('-' * 70)

				connection.recv(1024).decode()

			print ("Done transmission")
			connection.close()
		except socket.error:
			pass

HOST = str(sys.argv[1])

sender = messageSender(HOST, 4444, dataToTransmit) #PI IP ADDRESS
sender.start()
