# CSC591-791_Group1_Homework3
CSC 591/791 Group 1 (Omar Chedid, Anirudh Ganji, Athishay Kiran, Katherine Brown) Homework 3

### 1

Format of header and packet that goes from Rasp Pi to Arduino Uno via LED and Photodiode

### 2

Format of ACK that goes from laptop 2 to Rasp Pi via TCP connection over WiFi



### 3

How LED is modulated to transmit a 1 or a 0:

The LED is utilized with two output states: GPIO.LOW and GPIO.HIGH.  We have two options for transmission of 1 or 0.  If Manchester encoding is enabled, a 1 is signified by a GPIO.LOW output for one unit of time, defined by the value in the txDelay variable, followed by a GPIO.HIGH output for one unit of time.  Likewise, if Manchester encoding is enabled, a 0 is signified by a GPIO.HIGH output for one unit of time, followed by a GPIO.LOW output for one unit of time.  <p>In the event that Manchester encoding is not enabled, a 1 is signified by a GPIO.HIGH output for one unit of time and a 0 is signified by a GPIO.LOW output for one unit of time.

### 4

How the Rasp Pi and Arduino are synchronized:

We used Manchester encoding to synchronize the transmitter (Raspberry Pi) and the receiver (Arduino Uno). The signal transitions allow for clock information to be extracted directly from the data stream.

### 5

How long do you take to transmit a bit

### 6

Explanation of the scheme you use to build reliability
