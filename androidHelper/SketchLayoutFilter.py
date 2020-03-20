from Utils import XmlUtil
from resource.ElementData import ElementData
from androidHelper import SketchLayoutCreator
from functools import cmp_to_key

from Utils import Constants
class SketchLayoutFilter:
 
    

    def doFilter(self,document,anotateMap):
#         Update layout
        return self.doFilderInternal(document, anotateMap)

    def doFilderInternal(self, root, anotateMap):
        return 

    def anotate(self, document):
        elementDataMap = {}
        elements = list(document.iter())
        for node in elements:
            self.anotateIntenal(node, elementDataMap)
        return elementDataMap

# Annotate default attributes of all the UI element
    
    def anotateIntenal(self, root, elementDataMap):
        top = int (XmlUtil.getDipValue(root, Constants.ATTRIBUTE_LAYOUT_MARGIN_TOP))
        left = int(XmlUtil.getDipValue(root, Constants.ATTRIBUTE_LAYOUT_MARGIN_LEFT))
        width = int (XmlUtil.getDipValue(root,Constants.ATTRIBUTE_LAYOUT_WIDTH))
        height = int(XmlUtil.getDipValue(root,Constants.ATTRIBUTE_LAYOUT_HEIGHT))

        data = ElementData(top, left, width, height)
        elementDataMap[root] = data



    def isDefaultElement(self,element):
        return SketchLayoutCreator.FRAMELAYOUT_ELEMENT == element.tag
  