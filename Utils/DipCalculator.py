# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 00:08:24 2017

@author: soumi
"""
from Utils import Environment
from Utils import Constants

class Calculator:

    LDPI = 120
    MDPI = 160
    HDPI = 240
    XHDPI = 320
    XXHDPI = 480
    XXXHDPI = 640


    def __init__(self,forDeviceDensity):
        self.mForDeviceDensity = forDeviceDensity

        self.mprofileMap = {}

    def getPx(self, dp, value):
        px = dp * (value / self.mForDeviceDensity)
        return px
        
    

class Profile :

    def __init__(self, name,  _type,  width,  height) :
        self.mName = name
        self.mType = _type
        self.mWidth = width
        self.mHeight = height
        self.mDpWidth = (width * 160) /self.mType
        self.mDpTitleBarHeight = 0.2 * self.mType
        self.mDpHeight = ((height * 160) /self.mType) - self.mDpTitleBarHeight
#        self.mDpTitleBarHeight = dpTitleBarHeight
        
#    def screenShotProcess(self, img):
#        titleBarHeight = int(self.mDpTitleBarHeight/(2*(self.mDpTitleBarHeight + self.mDpHeight)) * self.mHeight)
#        imgNew = img[titleBarHeight:]
#        return imgNew
    
    

class DipCalculator:
    
    def __init__(self, rgbaImage, profile):
#        if profile == None: 
#            profile =  Profile("Nexus 5", Calculator.XXHDPI, Constants.DEFAULT_OUTPUT_SCREEN_WIDTH_PIXEL, Constants.DEFAULT_OUTPUT_SCREEN_HEIGHT_PIXEL,Constants.DEFAULT_SCREEN_WIDTH_DP, Constants.DEFAULT_SCREEN_CONTENT_VIEW_HEIGHT_DP, Constants.DEFAULT_SCREEN_TITLE_BAR_HEIGHT_DP)
#            profile =  Profile("Nexus 5", Calculator.XXHDPI, Constants.DEFAULT_OUTPUT_SCREEN_WIDTH_PIXEL, Constants.DEFAULT_OUTPUT_SCREEN_HEIGHT_PIXEL)
            
        self.mWidthPx = 0
        self.mHeightPx = 0
    
        if len(rgbaImage.shape) == 2 :
            self.mHeightPx, self.mWidthPx = rgbaImage.shape
        else:
            self.mHeightPx, self.mWidthPx,channels = rgbaImage.shape
        
        standardScreenWidthDpi = profile.mDpWidth
        standardScreenHeightDpi = profile.mDpHeight
        
#        if Environment.getValue(Environment.KEY_WITH_TITLE_BAR) == False:
#            standardScreenHeightDpi += profile.mDpTitleBarHeight

        scaleType = int(Environment.getValue(Environment.KEY_SCALE_TYPE))

        if scaleType== 3: 
            self.mWidthDpr = profile.mWidth / standardScreenWidthDpi
            # We just need the same dpr here, regardless of dpr of height,
            # because we don't want
            # the height of the output to scale to the screen size
            self.mHeightDpr = self.mWidthDpr

        elif scaleType== 1: 
             ratioWidth = self.mWidthPx / standardScreenWidthDpi
             ratioHeight = self.mHeightPx / standardScreenHeightDpi
            
             self.mWidthDpr = max(ratioWidth, ratioHeight)
             self.mHeightDpr = self.mWidthDpr
        else:
             self.mWidthDpr = self.mWidthPx / standardScreenWidthDpi
             self.mHeightDpr = self.mHeightPx / standardScreenHeightDpi
            

    def isViewToBeIgnore(self, width, height):
        return self.pxToHeightDip(height) * self.pxToWidthDip(width) < Constants.MIN_AREA_TO_IGNORE_RATIO_HEIGHT_DP * Constants.MIN_AREA_TO_IGNORE_RATIO_WIDTH_DP
    

    def isViewToBeIgnoreView(self, rectView):
        return self.isViewToBeIgnore(rectView.width, rectView.height)
    

    def pxToWidthDip(self,  px) :
        return px / self.mWidthDpr
    

    def pxToHeightDip(self,  px) :
        return px / self.mHeightDpr
    

    def dipToHeightPx(self,  height) :
        return height * self.mHeightDpr
    

    def dipToWidthPx(self,  dip) :
        return dip * self.mWidthDpr
    

    def pxToFontDip(self,  px) :
        return px / self.mHeightDpr
    

