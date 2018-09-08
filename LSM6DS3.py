#Created By
#Alessandro Serrapica
#alexserrapica@gmail.com

import sys
import time
import math

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.I2C as I2C

ADC_ref = 3.3

zero_x = 1.569
zero_y = 1.569
zero_z = 1.569

sensitivity_x = 0.3
sensitivity_y = 0.3
sensitivity_z = 0.3

class LSM6DS3:
    i2c = None
    tempvar = 0
    global accel_center_x
    accel_center_x = 0
    global accel_center_y
    accel_center_y = 0
    global accel_center_z
    accel_center_z = 0


    def __init__(self, address=0x6b, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(address)
        self.address = address
        dataToWrite = 0
        dataToWrite |= 0x03
        dataToWrite |= 0x00
        dataToWrite |= 0x10
        self.i2c.write8(0X10, dataToWrite)

        accel_center_x = self.i2c.readS16(0X28)
        accel_center_y = self.i2c.readS16(0x2A)
        accel_center_z = self.i2c.readS16(0x2C)


    def readRawAccelX(self):
    	output = self.i2c.readS16(0X28)
    	return output;

    def readRawAccelY(self):
    	output = self.i2c.readS16(0x2A)
    	return output;

    def readRawAccelZ(self):
    	output = self.i2c.readS16(0x2C)
    	return output;


    def getXRotation(self):
        value_y = self.readRawAccelY()
        value_z = self.readRawAccelZ()

        yv=(value_y/1024.0*ADC_ref-zero_y)/sensitivity_y
        zv=(value_z/1024.0*ADC_ref-zero_z)/sensitivity_z
        angle_x =math.atan2(-yv,-zv)*57.2957795+180

        return angle_x;

    def getYRotation(self):
        value_x = self.readRawAccelX()
        value_z = self.readRawAccelZ()

        xv=(value_x/1024.0*ADC_ref-zero_x)/sensitivity_x
        zv=(value_z/1024.0*ADC_ref-zero_z)/sensitivity_z
        angle_y =math.atan2(-xv,-zv)*57.2957795+180

        return angle_y;

    def getZRotation(self):
        value_x = self.readRawAccelX()
        value_y = self.readRawAccelY()

        xv=(value_x/1024.0*ADC_ref-zero_x)/sensitivity_x
        yv=(value_y/1024.0*ADC_ref-zero_y)/sensitivity_y
        angle_z =math.atan2(-yv,-xv)*57.2957795+180

        return angle_z;

    def readRawGyroX(self):
        output = self.i2c.readS16(0X22)
        return output;

    def readFloatGyroX(self):
        output = self.calcGyro(self.readRawGyroX())
        return output;
