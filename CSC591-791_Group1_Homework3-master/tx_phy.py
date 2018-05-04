import RPi.GPIO as GPIO
import time

class vlc_tx(object):
	"""docstring for vlc_tx"""
	def __init__(self,txDelay=None,ledPin=None,fecFactor=None,enableManchester=None):
		super(vlc_tx, self).__init__()
		if txDelay == None:
			self.txDelay = 1
		else:
			self.txDelay = txDelay

		if ledPin == None:
			self.ledPin = 3
		else:
			self.ledPin = ledPin

		if fecFactor == None:
			self.fecFactor = 3
		else:
			self.fecFactor = fecFactor

		if enableManchester == None:
			self.enableManchester = True
		else:
			self.enableManchester = enableManchester

		self.GPIO = GPIO
		self.GPIO.setmode(self.GPIO.BOARD)
		self.GPIO.setup(self.ledPin,self.GPIO.OUT)


	def fec_bit(self,bit):
		
		opList = []
		bitVal = int(bit)
		for x in range(self.fecFactor):
			opList.append(bitVal)
		
		return opList

	def send_data(self,bit_stream,enableManchester=None):
		if enableManchester == None:
			enableManchester = self.enableManchester
		for bit in bit_stream:
			op = self.fec_bit(bit)
			print op
			for bitVal in op:
				self.send_bit(bitVal,enableManchester)

	def send_bit(self,bit,enableManchester=None):
		if enableManchester == None:
			enableManchester = self.enableManchester
		if enableManchester == True:
			if bit == 1:
				self.GPIO.output(self.ledPin,self.GPIO.LOW)
				time.sleep(self.txDelay)
				self.GPIO.output(self.ledPin,self.GPIO.HIGH)
				time.sleep(self.txDelay)
			elif bit == 0:
				self.GPIO.output(self.ledPin,self.GPIO.HIGH)
				time.sleep(self.txDelay)
				self.GPIO.output(self.ledPin,self.GPIO.LOW)
				time.sleep(self.txDelay)
		else:
			if bit == 1:
				self.GPIO.output(self.ledPin,self.GPIO.HIGH)
				time.sleep(self.txDelay)
			elif bit == 0:
				self.GPIO.output(self.ledPin,self.GPIO.LOW)
				time.sleep(self.txDelay)

	def cleanup(self):
		self.GPIO.cleanup()