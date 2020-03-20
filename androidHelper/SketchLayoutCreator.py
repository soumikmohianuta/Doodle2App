from RectUtils import RectUtil
from Utils import Constants
from Utils import XmlUtil,TextUtils
from Utils import ColorUtil
from Utils.XmlUtil import selectColorMode
from resource.StyleWriter import StyleWriter
from resource.ColorWriter import ColorWriter
from resource.AndroidManifestWriter import AndroidManifestWriter
from resource.StringWriter import StringWriter

from Utils.ColorUtil import CColor
from Utils import ColorUtil

import resource.LayoutHelper as LayoutHelper
import os



# Info about the UI element
class ElementInfo :
    def __init__(self, element,  _id) :
        self.element = element
        self._id = _id
        
class ListWrapper :

    def __init__(self, _list):
        self._list = _list
        self.alignmentType = -1
        
    def size(self) :
        return len(self._list)
        
#@Override
    def __eq__(self,obj) :
        if obj is None:
            return self.size() == 0
        elif type(obj) != type(self):
            return False
        else:
            return self._list != obj._list
            
    def __hash__(self):
        return self._list
    


# Create sketch Layout        
class SketchLayoutCreator :
    def __init__(self, rootView,   appName, outProjectFolder,dipCalulator):
    
        self.mRootView = rootView
        self.mOutProjectFolder = outProjectFolder
        self.mDipCalculator = dipCalulator
        self.mWriter = StringWriter(appName)
        self.mStyleWriter =  StyleWriter()
        self.mColorWriter =  ColorWriter()
        androidManifestPath = os.path.join(outProjectFolder, "app", "src","main")
        self.mAndroidManifestWriter = AndroidManifestWriter(androidManifestPath)
        self.mIdMap = {}
        self.interestedIcons = {}
        self.mDrawableMap = {}
        self.mListViews = []



    def createDocument(self):        
        _map = {}
# create root element    
        rootElement = XmlUtil.createSketchRoot(self.mDipCalculator,LayoutHelper.FRAMELAYOUT_ELEMENT, self.mRootView, self.mColorWriter)
#  To fix the style color
        color = ColorUtil.cColortoInt(CColor.Black)
        self.mColorWriter.addResource(selectColorMode(color))
        color = ColorUtil.cColortoInt(CColor.Cyan)
        self.mColorWriter.addResource(selectColorMode(color))

# add childeren to the layout
        self.addChildrenLayout(rootElement, self.mRootView, 0, 0, _map)
        
        return rootElement
    

# update background color
    def updateColorBackground(self, root) :
        self.updateColorBackgroundInternal(root)
    
# update background color on each element recursively
    def updateColorBackgroundInternal(self, rectViewParent) :

        if(rectViewParent.mType == RectViewTypes.VIEW_TYPE_TEXT):
            color = ColorUtil.findDominateColorForTextView(rectViewParent, self.mImage)
            rectViewParent.mColor = color[0]
            rectViewParent.textColor = color[1]
        else:
            color = ColorUtil.findDominateColor(rectViewParent, self.mImage)
            rectViewParent.mColor = color
        children = rectViewParent.mChildren
        for rectView in children:
#            if rectView.mType != RectViewTypes.VIEW_TYPE_IMAGE:
                self.updateColorBackgroundInternal(rectView)
        
    
    def resetIdMap(self) :
        self.mIdMap = {}
        

    def isTextViewOrTextViewContainer(self, rectView) :
        if (rectView.mType == RectViewTypes.VIEW_TYPE_TEXT) :
            return True
        
        if len(rectView.mChildren) == 1 and rectView.mChildren[0].mType == RectViewTypes.VIEW_TYPE_TEXT:
            return RectUtil.same(rectView, rectView.mChildren[0], 0.1)
        
        return False
     

    def getId(self,  elementName) :
        index= 0
        if elementName in self.mIdMap:
            currentIndex = self.mIdMap[elementName]
            index = currentIndex + 1
        
        self.mIdMap[elementName] =  index
        return elementName + "_" + str(index)
    

# add children according to the category

    def addChildrenLayout(self, element, rectView,   parentLeft,   parentTop, rectViewElementInfoMap) :
        # Setting background
        
        for childRectView in rectView.mChildren:
            _id = ""
            # list view has it own index

            _id = self.getId(LayoutHelper.FRAMELAYOUT_ELEMENT)
            marginLeft = childRectView.x 
            marginTop = childRectView.y
            childElement = None
            childElement = XmlUtil.addElement(self.mDipCalculator, element,self.getElementTypeForRect(childRectView), childRectView,marginLeft, marginTop, _id, self.mColorWriter)
            
            rectViewElementInfoMap[childRectView] = ElementInfo( childElement, _id)
            self.addChildrenLayout(childElement, childRectView, childRectView.x, childRectView.y, rectViewElementInfoMap)
        

        XmlUtil.addBackgroundColor(element, rectView.mColor,self.mColorWriter)  
        
        
        if(rectView == self.mRootView):
            pass            
        
        # if children is icon add this attributes for code generation
        elif (rectView.isIconButton()) :              
              iconButtonName = rectView.getIconName()
              elementID = rectView.getElementID()
              element.tag = Constants.ELEMENT_IMAGE_BUTTON
              XmlUtil.addImageDrawable(element, iconButtonName)
              _id = self.getId(Constants.ELEMENT_IMAGE_BUTTON)

        # fit it to center
              XmlUtil.addAdditionalAttribute(element,"android:scaleType", "fitCenter")

        # add press animation              
              XmlUtil.addAdditionalAttribute(element,"android:background","@drawable/oniconpress")

              rectViewElementInfoMap[rectView] = ElementInfo(element, elementID)
        
        # if children is text add this attributes for code generation
        elif (rectView.isText()) :
            # default text hello text
             helloText = "Hello Text"
             stringId = self.mWriter.addResource(helloText)
             element.tag = Constants.ELEMENT_TEXT_VIEW
             
             XmlUtil.addSize(self.mDipCalculator, element, rectView.width,
                        rectView.height)
             

             XmlUtil.addBackgroundColor(element, rectView.mColor,self.mColorWriter)
             element.set(Constants.ATTRIBUTE_TEXT, XmlUtil.getReferenceResourceId(stringId))
             _id = self.getId(Constants.ELEMENT_TEXT_VIEW)
             XmlUtil.addId(element, _id)
             color = ColorUtil.cColortoInt(CColor.Black)
             XmlUtil.addTextColor(element, color,self.mColorWriter)
            # Set the auto text size property
             element.set(Constants.ATTRIBUTE_AUTOSIZE_TEXT_TYPE, "uniform")
             rectViewElementInfoMap[rectView] = ElementInfo(element, _id)
         
            # for all other UI elements   
        else:
            # for checkbox
            if (rectView.isCheckbox()) :
                _id = self.getId(Constants.ELEMENT_CHECK_BOX)
                element.tag = Constants.ELEMENT_CHECK_BOX
                # set checkbox default to uncheck
                XmlUtil.addAdditionalAttribute(element,"android:button", "@null")
                XmlUtil.addAdditionalAttribute(element,"app:theme", "@style/CheckboxStyle")
                XmlUtil.addAdditionalAttribute(element,"android:background","?android:attr/listChoiceIndicatorMultiple")
 
                # for Toggle
            elif (rectView.isToogle()) :
                element.tag = Constants.ELEMENT_SWITCH
                _id = self.getId(Constants.ELEMENT_SWITCH)
                minWidthDp = str(self.mDipCalculator.pxToWidthDip(rectView.width)-12) + Constants.UNIT_DIP 
                XmlUtil.addAttribute(element, "android:switchMinWidth",minWidthDp)
            
            # for Slider
            elif (rectView.isSlider()) :
                element.tag = Constants.ELEMENT_SEEK_BAR
                color = ColorUtil.cColortoInt(CColor.Black)
                XmlUtil.addAttributeColor(element, "android:progressTint", color,self.mColorWriter)
                XmlUtil.addAttributeColor(element, "android:thumbTint", color,self.mColorWriter)
                _id = self.getId(Constants.ELEMENT_SEEK_BAR)
                XmlUtil.addBackgroundColor(element, rectView.mColor,self.mColorWriter)
            
            # for star convert it to raing
            elif (rectView.isRating()) :

                element.tag = Constants.ELEMENT_RATING_BAR
                XmlUtil.addAttribute(element, "android:layout_width","wrap_content")
                XmlUtil.addAttribute(element, "android:layout_height","wrap_content")
                XmlUtil.addAttribute(element, "android:theme","@style/RatingBar")
                # based on the width of the element set number of star in rating
                widthOfStar =  int(self.mDipCalculator.pxToWidthDip(rectView.width)/50)
                _id = self.getId(Constants.ELEMENT_RATING_BAR)
                XmlUtil.addAttribute(element,"android:numStars", str(widthOfStar))
                
             # for Searchbar
            elif (rectView.isSearchBar()) :
                element.tag = Constants.ELEMENT_SEARCH_BAR
                _id = self.getId(Constants.ELEMENT_SEARCH_BAR)
                XmlUtil.addBackgroundColor(element, rectView.mColor,self.mColorWriter)

             # for Searchbar    
            elif (rectView.isUserImage()) :
                element.tag = Constants.ELEMENT_IMAGE_VIEW
                iconButtonName = "userimage"
                XmlUtil.addImageDrawable(element, iconButtonName)
                _id = self.getId(Constants.ELEMENT_IMAGE_VIEW)
             
                # for Container
            elif (rectView.isContainer()) :
                XmlUtil.addAttribute(element, "android:background","@drawable/border")
                _id = self.getId(LayoutHelper.FRAMELAYOUT_ELEMENT)
                
                # for Dropdown 
            elif (rectView.isDropDown()) :
                element.tag = Constants.ELEMENT_SPINNER
                XmlUtil.addAdditionalAttribute(element,"android:drawSelectorOnTop", "true")
                arrayId = self.mWriter.addArrayResource("default")
                # create a dummy array for the dropdown
                element.set(Constants.ATTRIBUTE_DROPDOWN_ENTRIES, XmlUtil.getArrayReferenceResourceId(arrayId))
                _id = self.getId(Constants.ELEMENT_SPINNER)
                element.attrib.pop("android:background", None)
                
                # for Text Button 
            elif (rectView.isButtonText()) :
                element.tag = Constants.ELEMENT_BUTTON
                XmlUtil.addAdditionalAttribute(element,"android:text", "Button")
                _id = self.getId(Constants.ELEMENT_BUTTON)
                XmlUtil.addAdditionalAttribute(element,"android:background","@drawable/oniconpress")

            XmlUtil.addId(element, _id)

            rectViewElementInfoMap[rectView] = ElementInfo(element, _id)
    

    def getElementTypeForRect(self, rectView) :
        return LayoutHelper.FRAMELAYOUT_ELEMENT
    
