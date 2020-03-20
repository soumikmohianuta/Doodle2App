# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 00:08:24 2017

@author: soumi
"""
## scale canvas pixels to android screen pixel 

class SketchDipCalculator:
    
    def __init__(self, width, height):
            
    
        self.mHeightPx=height
        self.mWidthPx = width
        
## default screen size considered for andorid code generation 
        standardScreenWidthDpi = 410
        standardScreenHeightDpi = 730
            
        self.mWidthDpr = self.mWidthPx / standardScreenWidthDpi
        self.mHeightDpr = self.mHeightPx / standardScreenHeightDpi
                
##convert px widht to dip
    def pxToWidthDip(self,  px) :
        return int(px / self.mWidthDpr)
    
##convert px height to dip
    def pxToHeightDip(self,  px) :
        return int(px / self.mHeightDpr)
    

##convert dip to px height
    def dipToHeightPx(self,  height) :
        return int(height * self.mHeightDpr)
    
##convert dip to px width
    def dipToWidthPx(self,  dip) :
        return int(dip * self.mWidthDpr)
        

