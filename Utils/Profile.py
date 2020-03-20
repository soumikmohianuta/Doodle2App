# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:54:05 2018

@author: soumi
#Help to store Phone display property
"""
from enum import Enum
class DeviceDensity(Enum):
    ldpi = 1
    mdpi = 2
    hdpi = 3
    xhdpi = 4
    xxhdpi = 5
    

class Profile :
#Help to store Phone display property
    def __init__(self,  devicetype,  width,  height) :
        self.mType = devicetype
        self.mWidth = width
        self.mHeight = height
        self.mDeviceDensity = self.typeToDensity()
        self.mDpWidth = (width * 160) /self.mDeviceDensity
        self.mDpWidth = (height * 160) /self.mDeviceDensity
        #Haven't cosidered title bar. Rather consider title bar heigt
        self.mDpTitleBarHeight = 0
        self.mDpHeight = ((height * 160) /self.mDeviceDensity) - self.mDpTitleBarHeight
        
    
    
    def typeToDensity(self):
        deviceDensity = 160
        if(self.mType == DeviceDensity.ldpi):
            deviceDensity = 120
        elif(self.mType == DeviceDensity.hdpi):
            deviceDensity = 240
        elif(self.mType == DeviceDensity.xhdpi):
            deviceDensity = 320  
        elif(self.mType == DeviceDensity.xxhdpi):
           deviceDensity = 480
        return deviceDensity