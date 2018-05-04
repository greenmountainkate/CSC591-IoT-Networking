# Homework 2 - Raspberry Pi B 

The Raspberry Pi B is a MQTT client which subscribes to the topics "lightStatus", "Status/RaspberryPiA", and "Status/RaspberryPiC".  It is connected to three LEDs which reflect the state of the Raspberry Pi A, Raspberry Pi C, and the LightStatus.  It uses the information it receives to make a determination as to which LEDs should be lit at any given time.

## Requirements

### Necessary Operating System, Packages, and Libraries

This project requires an installed version of Mosquitto MQTT and Python.  To be run on Fedora 27 OS, other necessities can be installed using the following commands:

```
sudo dnf install redhat-rpm-config
```
```
sudo dnf install python3-devel
```
```
pip install Adafruit_MCP3008
```
```
pip install Adafruit_GPIO
```
```
pip install paho-mqtt
```

### Software Setup

To execute file, run the following command in terminal:

```
python3 pi_B_client.py <broker IP address> <Pin 1 GPIO> 
      <Pin 2 GPIO> <Pin 3 GPIO>
```

### Hardware Setup

<img src="https://github.ncsu.edu/kmbrown/CSC591-791_Group1_Homework2/blob/master/circuit2_bb.jpg" width=300>

## Software Functionality
### Functions

def setup_pins(pin1, pin2, pin3):

def on_connect(client, userdata, flags, rc):

def on_disconnect(client, userdata, rc):

def on_publish(client, userdata, mid):
      
def on_subscribe(client, userdata, mid, granted_qos):

def on_unsubscribe(client, userdata, mid):

def on_message(client, userdata, message):       

def ledStatus(status, pin):
  
### Flow of Control
  Upon execution of pi_B_client.py, the program establishes a connection with the port provided in the command line, publishes a message "online" to the topic "status/raspberrypiB", and subscribes to topics "lightStatus", "status/raspberrypiA", and "status/raspberrypiC".  Upon receiving a message from topic "lightStatus" with the value "turnOn" the program will set the LIGHT_STATUS to True and the LED 1 will be lit. Upon receiving a message from the topic "lightStatus" with the value "turnOff" the program will set the LIGHT_STATUS to False and LED 1 will be turned off.  Upon receiving a message from the topic "status/raspberrypiA" with the topic "online", PI_A_STATUS will be set to True and LED 2 will be lit.  Upon receiving a message from the topic "status/raspberrypiA" with the topic "offline", PI_A_STATUS will be set to False and LED 2 will be turned off.  Upon receiving a message from the topic "status/raspberrypiC" with the topic "online", PI_C_STATUS will be set to True and LED 3 will be lit.  Upon receiving a message from the topic "status/raspberrypiC" with the topic "offline", PI_C_STATUS will be set to False and LED 3 will be turned off.  Upon disconnection, either due to network interruption or to graceful disconnect, a message containing "offline" will be published to the topic "status/raspberrypiB".

## Role in Overall System

  The Raspberry Pi B is the actuator portion of the overall system.  It uses the information received from the publishers to turn LEDs on and off, to reflect the states of the publishers and the sensor information.
