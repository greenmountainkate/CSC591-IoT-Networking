# Homework 2 - Raspberry Pi C 

The Raspberry Pi C subscribes to the topics "lightSensor" and "threshold" which are published by Pi A.  Upon receiving new information from those topics, Pi C runs a comparison of the values and generates a binary result.  If that result has changed from the previous result, the Pi C will publish the change to the topic, "lightStatus".  Pi C also publishes its status to the topic "Status/RaspberryPic".

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
python3 pi_C_client.py <broker IP address> 
```

### Hardware Setup

Raspberry Pi connected via WIFI to MQTT Broker.  No other hardware necessary.

## Software Functionality
### Functions
def on_connect(client, userdata, flags, rc):

def on_disconnect(client, userdata, rc):
       
def on_publish(client, userdata, mid):
       
def on_subscribe(client, userdata, mid, granted_qos):
       
def on_unsubscribe(client, userdata, mid):
       
def on_message(client, userdata, message):
  
### Flow of Control
  Upon execution of pi_C_client.py, the program establishes a connection through the port provided in the command line, publishes a message of "online" to the topic "status/raspberrypiC", and subscribes to the topics "lightSensor", "threshold", and "lightStatus".  Upon receiving the first published values for topics "lightSensor" and "threshold", the program will compare the values.  If the value for the lightSensor is higher than the value for the threshold, the value for newLightStatus will be set to "turnOff", otherwise it will be set to "turnOn".  Next, the value for newLightStatus will be compared to be the previously published value of the topic "lightStatus".  If the two are not equal, the program will publish the current value of newLightStatus to the topic "lightStatus", otherwise, the program will continue.  Upon disconnection, either due to interruption or graceful disconnect, the topic "status/raspberrypiC" will publish a message with the topic "offline".


## Role in Overall System

Raspberry Pi C is the decision making segment of the system.  It intakes sensor values, compares them to one another, and determines whether the LED needs to be turned on, turned off, or left unchanged.  That information is then published to Pi B, which completes the action.



