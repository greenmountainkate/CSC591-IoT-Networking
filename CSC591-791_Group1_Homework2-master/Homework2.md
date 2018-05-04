# CSC 591/791 Group1 - Homework 2
Group Members: Omar Chedid, Anirudh Ganji, Athishay Kiran, Katherine Brown

### Group Member Contributions

 | Member Name     |  Contribution % |
 |-----------------|-----------------|
 | Omar Chedid     |       25%       |
 | Athishay Kiran  |       25%       |
 | Anirudh Ganji   |       25%       |
 | Katherine Brown |       25%       |
 
 

 |  Subtasks       |  Omar Chedid    |  Athishay Kiran  |  Anirudh Ganji  |  Katherine Brown  |
 |-----------------|-----------------|------------------|-----------------|--------------------------|
 | Project Design  |25%|25%|25%|25%|
 | Software Design |40%|20%|20%|20%|
 | Software Exec   |40%|20%|20%|20%|
 | S - PiA Client  |40%|20%|20%|20%| 
 | S - PiB Client  |40%|20%|20%|20%| 
 | S - PiC Client  |40%|20%|20%|20%| 
 | S - Broker      |25%|25%|25%|25%| 
 | Hardware Design |20%|40%|20%|20%|
 | Hardware Exec   |20%|30%|30%|20%|
 | Hardware PiA    |20%|40%|20%|20%|
 | Hardware PiB    |20%|40%|20%|20%|
 | Hardware PiC    |20%|40%|20%|20%|
 | Testing         |25%|25%|25%|25%|
 | Testing Software|20%|20%|40%|20%|
 | Testing Hardware|20%|20%|40%|20%|
 | Documentation   |20%|20%|20%|40%|
 | Schematics      |20%|20%|20%|40%|
 
### Schematics

<img src="https://github.ncsu.edu/kmbrown/CSC591-791_Group1_Homework2/blob/master/circuitSchematic1.jpg" width=450>

### Design Choices
- MQTT Broker Choice:
 We chose to use Mosquitto as our MQTT broker due to its maturity, extensive documentation, and open source availablity.
 
- Installation instructions:
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
 - The ADC sampling frequency was 100 milliseconds.
 
 - We chose not to scale the values, as we implemented using a threshold value comparison of 50.

  - Raw value range from ADC from Potentiometer: 0 - 1024

  
