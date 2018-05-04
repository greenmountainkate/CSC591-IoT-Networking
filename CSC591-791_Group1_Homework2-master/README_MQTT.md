# Homework 2 - MQTT Broker

The MQTT broker is a Mosquitto broker running on Fedora Linux, connected via wifi port with Raspberry Pi A, Raspberry Pi B, and Raspberry Pi C.


## Requirements

This project requires an installed version of Mosquitto MQTT service.

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
 To enable the MQTT broker, run the following commands:
 ```
 systemctl enable mosquitto.service
 ```
 ```
 systemctl start mosquitto.service
 ```


## Role in Overall System

The MQTT broker facilitates the movement of information throughout the system.

## Licenses

Mosquitto is used under the EPL/EDL licenses from Eclipse


