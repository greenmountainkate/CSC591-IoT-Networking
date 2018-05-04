#include <Wire.h>

long accelX, accelY, accelZ;
float gForceX, gForceY, gForceZ;

long gyroX, gyroY, gyroZ;
float rotX, rotY, rotZ;

void setup() {
  Serial.begin(2000000);
  Wire.begin();
  setupMPU();

}

void loop() {
  
  recordAccelRegisters();
  recordGyroRegisters();
  printData();
  delay(5);
  

}

void setupMPU() {
  Wire.beginTransmission(0b1101000); //I2C addy of the MPU per manual
  Wire.write(0x6B); //Accesses register 6B - power management per manual section 4.28 allows to configure clock mode and manage sleep mode
  Wire.write(0b00000000); //Setting sleep register to 0
  Wire.endTransmission();
  Wire.beginTransmission(0b1101000); //I2C addy of the MPU
  Wire.write(0x1B); //Accesses register 1B - Gyro config 
  Wire.write(0x00000000); //Set gyro to full +/-250 degree/second - can go up to 2000
  Wire.endTransmission();
  Wire.beginTransmission(0b1101000); //I2C addy 
  Wire.write(0x1C); //Accesses register 1C - Accel config
  Wire.write(0b00000000); // set accel to +/- 2g - can go up to 16g
  Wire.endTransmission();
}

void recordAccelRegisters(){
  Wire.beginTransmission(0b1101000); //I2C addy of the MPU per manual
  Wire.write(0x3B); //start reg for accel reads
  Wire.endTransmission();
  Wire.requestFrom(0b1101000, 6);  //Request Accel Reg (3B - 40) that take measurements
  while(Wire.available() < 6);
  accelX = Wire.read() <<8|Wire.read(); //Store first two bytes in accelX
  accelY = Wire.read() <<8|Wire.read(); //Store middle two bytes in accelY
  accelZ = Wire.read() <<8|Wire.read(); //Store last two bytes in accelZ
  processAccelData();
}

void processAccelData(){
  gForceX = accelX/16384.0; //convert to measurement in g based on input as 2g range
  gForceY = accelY/16384.0; //ditto
  gForceZ = accelZ/16384.0; //ditto
}

void recordGyroRegisters(){
  Wire.beginTransmission(0b1101000); //I2C addy
  Wire.write(0x43); //Start reg for gyro
  Wire.endTransmission();
  Wire.requestFrom(0b1101000, 6); //Request Gyro reg (43 - 48) records gyro measurements
  while(Wire.available() < 6);
  gyroX = Wire.read() <<8|Wire.read(); //Store first 2 bytes in X
  gyroY = Wire.read() <<8|Wire.read(); //Store middle 2 bytes in Y
  gyroZ = Wire.read() <<8|Wire.read(); //Store last 2 bytes in Z
  processGyroData();
  
}

void processGyroData(){
  rotX = gyroX / 131.0; //convert to measurement in degrees, based on 250 degree/second setting
  rotY = gyroY / 131.0; // ditto
  rotZ = gyroZ / 131.0; //ditto
  
}

void printData(){
  Serial.println("Begin");
  String xForceString = String(gForceX);
  Serial.println(xForceString);
  String yForceString = String(gForceY);
  Serial.println(yForceString);
  String zForceString = String(gForceZ);
  Serial.println(zForceString);
  String xAccelString = String(rotX);
  Serial.println(xAccelString);
  String yAccelString = String(rotY);
  Serial.println(yAccelString);
  String zAccelString = String(rotZ);
  Serial.println(zAccelString);
  Serial.println("End"); 
  //Serial.println(%f, %f, %f, %f, %f, %f, gForceX, gForceY, gForceZ, rotX, rotY, rotZ);  
}


