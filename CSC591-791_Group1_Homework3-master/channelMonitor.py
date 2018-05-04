import socket
import sys
import binascii
import threading


class ChannelHandler():
	def __init__(self, ipAddress, port):
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.ipAddress = ipAddress
		self.port = port

		print("Created Server Socket For Channel Updates")
		try:
			self.serverSocket.bind((self.ipAddress, self.port))
			while True:
				self.serverSocket.listen(1)
				connection, address = self.serverSocket.accept()
				channelHandlerThread = ChannelHandlerThread(address[0], address[1], connection)
				channelHandlerThread.start()
		except KeyboardInterrupt:
			pass

		self.serverSocket.close()
		print("Killing server")

########################################################################################################
class ChannelHandlerThread(threading.Thread):
	def __init__(self, clientIP, clientPort, clientSocket):
		threading.Thread.__init__(self)
		self.clientIP = clientIP
		self.clientPort = clientPort
		self.connection = clientSocket

	def run(self):
		channelUpdate = str(self.connection.recv(1024).decode())
		print ("New Channel Update: ")
		if (channelUpdate == "ALIVE"):
			print ("Channel [ONLINE]")
		elif (channelUpdate == "DEAD"):
			print ("Channel [OFFLINE]")

		self.connection.close()

########################################################################################################

HOST = str(sys.argv[1])

channelHandler = ChannelHandler (HOST, 9990)
