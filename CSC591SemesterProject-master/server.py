# processing script
import socket
import threading
import time

valueArray = []


def startPiData(conn,addr):
	print 'Connection from : ',addr
	
	while True:
		data = conn.recv(1024)
		
		if data == 'END':
			break
		elif data.split(' ')[0] == 'File':
			fileName = 'output_{}'.format(data.split(' ')[1])
			fh = open(fileName,'w')	
			continue
		else:	
			fh.write(data)
			fh.write('\n')
	fh.close()

d1_done = False
d2_done = False
PORT = 5050
soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

soc.bind(('',PORT))
soc.listen(10)

# fh = open('output','w')
# conn1,addr1 = soc.accept()
# conn2,addr2 = soc.accept()

# now = time.time()
# while time.time()-now < 10:
# 		data1 = conn1.recv(1024)
# 		fh.write(data1)
# 		fh.write('\n')
# 		data2 = conn2.recv(1024)
# 		fh.write(data2)
# 		fh.write('\n')

# 		if data1 == 'END':
# 			d1_done = True
# 		if data2 == 'END':
# 			d2_done = True
# 		if d1_done and d2_done:
# 			break
		
while True:
	conn,addr =  soc.accept()
	t = threading.Thread(target=startPiData,args=(conn,addr))
	t.start()
	
# Total sensors of each Pi = 7

# Total Pis = 2


# Read each file

	# get the start time stamp, append to start time buffer

		# apply [0/1] decision on each sensor value 
		# append the value to the global buffer

	# get the end time stamp append to endtime buffer

# apply decision on global buffer
	
	# if step detected, get time stamp and sensor ids (location)
	
	# append time stamp, position to dictionary
