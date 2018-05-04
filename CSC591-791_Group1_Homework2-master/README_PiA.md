# Homework 2 - Raspberry Pi A 

The Raspberry Pi A is both a publisher and a subscriber that samples from an LDR and a potentiometer, every 100 milliseconds.  A comparison is made between the values and the previously measured values.  If the difference is over a preset threshold value, the new values are published.  LDR values are published to topic "lightSensor" and potentiometer values are published to topic "threshold".

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

To execute file, run following command in terminal:
```
python3 pi_A_client.py <broker IP address> <LDR sensitivity>
  <potentiometer sensitivity> <LDR channel on ADC> 
  <potentiometer channel on ADC>
```

### Hardware Setup

<img src="https://github.ncsu.edu/kmbrown/CSC591-791_Group1_Homework2/blob/master/circuit1_bb.jpg" width=300>

## Software Functionality
### Functions
  on_connect( client, userdata, flags, rc ):
     
  on_disconnect( client, userdata, rc=0 ):
  
  on_publish( client, userdata, mid ):
  
  on_subscribe( client, userdata, mid, granted_qos ):
  
  on_unsubscribe( client, userdata, mid ):
  
  on_message( client, userdata, message ):
  
### Flow of Control
  Upon execution of pi_A_client.py, the program connects to the port provided in the command line, publishes the message "online" to the topic "status/raspberrypiA", subscribes to the topics "lightSensor" and "threshold" and begins taking readings from the LDR and potentiometer settings.  The initial reading is automatically reported to both topics.  If subsequent readings on either sensor have changed, the new reading will be reported to the relevant topic.  Upon disconnection, either due to a lost connection or a graceful disconnect, the message "offline" will be published to the topic "status/raspberrypiA".   

## Role in Overall System

Raspberry Pi A is the sensor portion of the system.  Pi A collects information from the LDR and potentiometer sensors and determines whether that information has shifted enough to warrent notifying the rest of the system.   Raspberry Pi A also subscribes to the topics it publishes, to use the previous published values in its comparison.

