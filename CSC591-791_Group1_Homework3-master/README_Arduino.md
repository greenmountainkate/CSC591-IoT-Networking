# Homework 2 - Arduino Uno 

The Arduino UNO is acting as an analog receiver in this system.  It is connected to a photodiode, takes readings at regular intervals, and passes the values as Strings to laptop 2 via USB connection at port dev/cu.usbmodem1411.
## Requirements

### Necessary Operating System, Packages, and Libraries

This project requires a working copy of arduino installed on the computer that is uploading the sketch to the Arduino.  On Fedora 27, the command for that installation is:
```
sudo dnf install arduino
```

### Software Setup

The sketch is uploaded via the Arduino IDE via the following sequence:
  - connect the Arduino via USB
  - compile sketch
  - Choose board to upload sketch onto
  ```
  Tools -> Board -> Arduino Uno
  ```
  - select serial port
  
 ```
 Tools -> Board -> Port
 ```
 - Press upload button to send sketch to Arduino Board
 
 As long as the board is powered on, the sketch will run its setup() and loop() functions.

### Hardware Setup

<img src="https://github.ncsu.edu/kmbrown/CSC591-791_Group1_Homework3/blob/master/circuitSchematic1.jpg" width=500>

## Software Functionality
### Functions

void setup()
    //initializes serial communication at 2000000 bits/sec
    
void loop()
    //reads input on analog pin 0
    //prints analog value read as 
    //delays for stability

  
### Flow of Control
 On powerup, the sketch will execute automatically.  The setup() function runs, which establishes serial communication at 2000000 bits/sec.  The loop() function runs continuously, monitoring the photodiode at analog pin 0, and writing that value via the serial port over USB to laptop 2.
 
## Role in Overall System

The Arduino acts as the analog receiver, monitoring the values recorded by the photodiode sensor and reporting those values to the receiver program running on laptop 2.


