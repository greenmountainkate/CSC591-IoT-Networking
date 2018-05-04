import socket
import sys
import threading
import time

import tx_phy

phyObj = tx_phy.vlc_txt(txDelay=0.0008, fecFactor=1, enableManchester=True)


channelAlive=None

class ClientThread(threading.Thread):

        
        def __init__(self, clientIP, clientPort, clientSocket, server):
            threading.Thread.__init__(self)
            self.clientIP = clientIP
            self.clientPort = clientPort
            self.connection = clientSocket
            self.server = server
            self.clientType = None
            

        def run (self):

            print("Started thread "+str(threading.current_thread().getName()))
            self.clientType = str(self.connection.recv(1024).decode())
 
            if (self.clientType=="SEND"):
                print ("SEND RECEIVED")
                self.connection.sendall("OK")
                numberOfChunks = int(self.connection.recv(1024).decode())
                self.connection.sendall("OK")


                for i in range(numberOfChunks):
                    messageToSend = str(self.connection.recv(1024).decode())
                    if (i%2==0):
                        self.server.ACKZERO=False
                    else: self.server.ACKONE=False

                    self.connection.sendall("BUSY")
                    self.connection.recv(1024).decode() ##OK

                    
                    if (i%2==0):
                        while (self.server.ACKZERO == False):
                            print ("Sending "+ messageToSend)
                            print ("WAITING FOR ACK 0")
                            phyObj.send_data(messageToSend)
                            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            #s.connect((self.server.PC1ADDR, 6666))
                            #s.sendall(messageToSend)
                

                            time.sleep(5)               #DEFINE TIMEOUT HERE
                        self.connection.sendall("AVAILABLE")
                        self.connection.recv(1024).decode()
                    else:
                        while (self.server.ACKONE == False):
                            print ("Sending "+ messageToSend)
                            print ("WAITING FOR ACK 1")        #DELETE THIS
                            phyObj.send_data(messageToSend)
                            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            #s.connect((self.server.PC1ADDR, 6666))
                            #s.sendall(messageToSend)

                            time.sleep(5)               #DEFINE TIMEOUT HERE
                        self.connection.sendall("AVAILABLE")
                        self.connection.recv(1024).decode()
                    self.connection.sendall("OK")

            if (self.clientType=="ACK0"):
                self.server.ACKZERO = True
                channelUpdate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                channelUpdate.connect((self.server.PC1ADDR, 9990))
                channelUpdate.sendall("ALIVE")
                channelUpdate.close()
            
                print ("ACK 0 RECEIVED")

            if (self.clientType=="ACK1"):
                self.server.ACKONE = True
                channelUpdate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                channelUpdate.connect((self.server.PC1ADDR, 9990))
                channelUpdate.sendall("ALIVE")
                channelUpdate.close()
                print ("ACK 1 RECEIVED")

            if (self.clientType=="DEAD"):
                channelUpdate = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                channelUpdate.connect((self.server.PC1ADDR, 9990))
                channelUpdate.sendall("DEAD")
                channelUpdate.close()
                print ("DEAD RECEIVED")

            
            print ("Killing thread "+str(threading.current_thread().getName()))
            self.connection.close()




################################################################################################


class Server():
    def __init__(self, HOST, PORT, PC1ADDR):
        self.HOST = HOST
        self.PORT = PORT
        self.PC1ADDR = PC1ADDR
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.ACKZERO = None
        self.ACKONE = None

        print("Created Server Socket")

        try:
            self.serverSocket.bind((self.HOST, self.PORT))
        except:
            print("Cant bind to port "+str(self.PORT))
            sys.exit()
        print("Binding server to port "+str(self.PORT))

        while True:
            self.serverSocket.listen(1)
            print("Listening for new connections")
            connection, address = self.serverSocket.accept()
            print("Connected to client with IP address "+str(address[0]))
            clientThread = ClientThread(address[0], address[1], connection, self)
            clientThread.start()
        self.serverSocket.close()

################################################################################################

HOST = str(sys.argv[1])         #IP ADDRESS OF THIS DEVICE (PI)
PC1ADDR = str(sys.argv[2])      #IP ADDRESS OF PC1
server = Server(HOST,4444, PC1ADDR)





