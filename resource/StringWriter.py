from Utils import XmlUtil
from Utils import Constants
from Utils import TextUtils
from resource import TextResource
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


class StringWriter(TextResource.TextResource):
#    private final String mAppName;

    def __init__(self,appName):
        super().__init__()
        self.mAppName = appName
        self.mRoot = Element(Constants.ELEMENT_RESOURCE)
        element =  SubElement (self.mRoot, Constants.ELEMENT_STRING)
        element.set(Constants.ATTRIBUTE_NAME, "app_name")
        element.text = TextUtils.formatText(self.mAppName)
        self.mDataIndexMap = {}
        self.mArrayDataIndexMap = {}
        self.mId= 0
        self.mArrayID = 0
    def addResource(self,value):
        formatText = TextUtils.formatText(value)
        _id = "string_"
        if  formatText in self.mDataIndexMap:
            index = self.mDataIndexMap[formatText]
            _id += str(index)
        else:
            _id += str(self.mId)
            self.mDataIndexMap[value] = self.mId
            self.mId = self.mId + 1
            element = SubElement(self.mRoot, Constants.ELEMENT_STRING)
            element.set(Constants.ATTRIBUTE_NAME, _id)
            element.text = formatText
        return _id

    def addArrayResource(self,value):
        _id = "string_array_"
        if  value in self.mArrayDataIndexMap:
            index = self.mDataIndexMap[value]
            _id += str(index)
        else:
            _id += str(self.mId)
            self.mDataIndexMap[value] = self.mArrayID
            self.mArrayID = self.mArrayID + 1
            element = SubElement(self.mRoot, Constants.ELEMENT_STRING_ARRAY)
            element.set(Constants.ATTRIBUTE_NAME, _id)
            subElement1 = SubElement(element, "item")
            subElement1.text = "Item 1"
            subElement2 = SubElement(element, "item")
            subElement2.text = "Item 2"
            subElement3 = SubElement(element, "item")
            subElement3.text = "Item 3"

        return _id