import binascii
import socket
import sys
import time
HOST = str(sys.argv[1])
PORT = int(sys.argv[2])
ACKHOST= "127.0.0.1"
ACKPORT= 4444

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

def ackFunction(text):
	ackUpdate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ackUpdate.connect((ACKHOST, ACKPORT))
	ackUpdate.sendall(text)
	ackUpdate.close()

packetBitSize=64
packetByteSize=packetBitSize/8
startStr="0START"
doneStrO="1DONE"
doneStrZ="0DONE"
newSize=packetByteSize+1
startStr=startStr.ljust(newSize)
doneStr0=doneStrZ.ljust(newSize)
doneStr1=doneStrO.ljust(newSize)
startBin=toBinary(startStr)
doneBin0=toBinary(doneStr0)
doneBin1=toBinary(doneStr1)
readFlag=0
wordList=[]
dStr=""
doneFlag=0
prev="-1"


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.bind((HOST,PORT))
connection.listen(2)
conn,addr = connection.accept()

while True:
	time.sleep(5)
	print 'Here'
	failFlag=0
	binVal=str(conn.recv(1024).decode())

	else:
		try:
			print binVal
			val=fromBinary(binVal)
		except:
			print "Conversion Failed, need to send NACK or FAIL to PC1"
			failFlag=1
	
		if failFlag==0:
			
			if val=="FAIL":
				print "Link Broken!"
				ackFunction("DEAD")
				dstr=""
				prev="-1"
				wordList=[]
				readFlag=0

			if(readFlag==0):
				if(startStr==val):
					readFlag=1
					prev=val[0]
					ackVal="ACK"+val[0]
					ackFunction(ackVal) 
				else:
					pass

			elif(readFlag==1):
				if(val[0]==prev):
					pass # Received same packet again. 
				else:
					if((val==doneStr0) or (val==doneStr1)):
						ackVal="ACK"+val[0]
						ackFuncation(ckVal)
						readFlag=0
						doneFlag=1
					else:
						ackVal="ACK"+val[0]
						ackFunction(ackVal)
						actual=val[1:]
						wordList.append(actual)

	if doneFlag==1:
		doneFlag=0
		l=len(wordList)
		lastStr=wordList[l-1]
		lastList=lastStr.split()
		for i in range (0,l-1):
			dStr=dStr+wordList[i]
		l2=len(lastList)
		for i in range (0,l2):
			dStr=dStr+lastList[i]
		print "Data sent by PC1 is: ",dStr
		dStr="" # Clearing the data string
		wordList=[] # Clearing the binary list
