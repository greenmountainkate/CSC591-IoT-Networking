# Homework 2 - MQTT Clien

The MQTT client is a Mosquitto client running on Linux, connected via wifi port with Raspberry Pi A, Raspberry Pi B, and Raspberry Pi C.


## Requirements

This project requires an installed version of Mosquitto MQTT service and Python.

On Fedora 27 OS, install MQTT with following commands:
 ```
 sudo dnf install mqtt
 ```
 ```
 sudo dnf install mosquitto
 ```
 ```
 sudo dnf install mosquitto-clients
 ```
 To enable the MQTT client, run the following commands:
 ```
 systemctl enable mosquitto.service
 ```
 ```
 systemctl start mosquitto.service
 ```
 This also requires the Paho MQTT package for Python which can be installed with the following command:
 ```
 pip install paho-mqtt
 ```
## Execution
To execute file, run the following command in terminal:
```
python3 pc_2_client.py <Broker IP Address>
```
## Software Functionality

### Functions

def on_disconnect(client, userdata, rc):

def on_message(client, userdata, message):

### Flow of Control

On execution, the program connects to the port provided in the command line and subscribes to the topics: "lightSensor", "threshold", "lightStatus", "status/raspberrypiA", "status/raspberrypiB", and "raspberrypiC".  Upon receiving a message from any of those topics, a message is printed to a log containing the message payload and a timestamp.

## Role in Overall System

The MQTT client tracks the movement of messages through the system and reports them in a log.

## Licenses

Mosquitto is used under the EPL/EDL licenses from Eclipse

