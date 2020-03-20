from Utils import Util
from Utils import XmlUtil
from Utils import Constants
from androidHelper.SketchDipCalculator import SketchDipCalculator
import os
from androidHelper.SketchProjectInfo import SketchProjectInfo
from androidHelper import SketchProjectGenerator
from androidHelper.SketchLayoutCreator import SketchLayoutCreator
from androidHelper.SketchLayoutFilter import SketchLayoutFilter
from androidHelper.SketchRelativeLayoutFilter import SketchRelativeLayoutFilter
#from layout.RootAlignmentLayoutFilter import RootAlignmentLayoutFilter
from RectUtils.RectObj import RectObj
from RectUtils.Rect import Rect 
from RectUtils import RectUtil

#CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600

# generate project name for android
def generateProjectName(mFileName):
    filename, file_extension = os.path.splitext(mFileName)
    mProjectName = Util.getProjectName(filename)
    return mProjectName

# if only children and text area is more than 35% of container convert it to Text Button

def isTextButton(rectObj):

    if (len(rectObj.mChildren)==1) and rectObj.mChildren[0].isText() and (rectObj.mChildren[0].rectArea/rectObj.rectArea)>0.35 :
        return True
    else:
        return False

# search for text button in the hierarchy
def searchForTextButton(rectPar):
    for rectObj in rectPar.mChildren:
        if isTextButton(rectObj):
            rectObj.mChildren = []
            rectObj.iconID= 21
        else:
            searchForTextButton(rectObj)

# create hierachy from array of rects            
def createHierachy(rects, width, height):
    rootObj= RectObj(Rect(0,0,width,height))
    sortedRectObjs = sorted(rects, key=lambda x: x.rectArea)
    elementLength = len(sortedRectObjs)
    if(elementLength==1):
         rootObj.mChildren.append(sortedRectObjs[0])
         return rootObj
     
    # iterate through all rects create a hierarchy of all UI element
    for i in range(elementLength-1):
        item=sortedRectObjs[i]
        validElement = True
        isChild = False
        for j in range(i+1,elementLength):
            parItem = sortedRectObjs[j]
            if parItem != item:
                item, validElement, isChild = RectUtil.fixHierarchy(parItem,item,width,height)
                if isChild:
                    parItem.mChildren.append(item)
                    break
                if not validElement:
                    break
        if validElement and not isChild:            
            rootObj.mChildren.append(item)
    rootObj.mChildren.append(sortedRectObjs[elementLength-1])
    searchForTextButton(rootObj)
    return rootObj


# json returned by canvas convert it to rect object
def jsonToRect(jsonRects,dipCalulator):
    rectObjs=[]
    for item in jsonRects:
        rectObj = RectObj(Rect(int(item['x']),int(item['y']),int(item['width']),int(item['height'])),int(item['iconID']),int(item['elementId']))
        if rectObj.isRating():
            rectObj.width = dipCalulator.dipToWidthPx(50)
        if rectObj.isSearchBar():
            rectObj.width = dipCalulator.dipToWidthPx(50)
            rectObj.height = dipCalulator.dipToHeightPx(50)
        rectObjs.append(rectObj)
    return rectObjs


# generate project

def generateProject(rectViews, projectFolder, templateFolder, canvas_width,  projectName="SketchToUI"):
    CANVAS_WIDTH = canvas_width
    dipCalulator = SketchDipCalculator(CANVAS_WIDTH, CANVAS_HEIGHT)
    
    mOutProjectFolder =  os.path.join(projectFolder,projectName )
    
    rawRects = jsonToRect(rectViews,dipCalulator)
    
#    return 
    rootView = createHierachy(rawRects, CANVAS_WIDTH,CANVAS_HEIGHT)
    
    mProjectName = generateProjectName(projectName)


    
    SketchProjectGenerator.setup(projectFolder, templateFolder)
   
    
#    mDrawableWriter = DrawableWriter(file_extension, mOutProjectFolder)
    creator = SketchLayoutCreator(rootView, mProjectName, mOutProjectFolder,dipCalulator)

# create layout
    layoutDocument = creator.createDocument()
    layoutFilter = SketchLayoutFilter()
#
    anotateMap = layoutFilter.anotate(layoutDocument)

    layoutFilter = SketchRelativeLayoutFilter()
    layoutFilter.doFilter(layoutDocument, anotateMap)
    layoutFilter = SketchLayoutFilter()
    layoutFilter.doFilter(layoutDocument, anotateMap)
    mainXmlPath = os.path.join(mOutProjectFolder,"app", "src","main", "res", "layout", "activity_main.xml")

# write to xml
    XmlUtil.writeDocumentxml(layoutDocument,mainXmlPath)

# write style
#    styleWriter = creator.mStyleWriter
#    styleDocument = styleWriter.mRoot
#    styleDocumentPath = os.path.join(mOutProjectFolder, "app", "src","main","res","values","styles.xml")
#    XmlUtil.writeDocumentxml(styleDocument, styleDocumentPath)
#
#write to color file    
    colorWriter = creator.mColorWriter
    colorDocument = colorWriter.mRoot
    colorDocumentPath = os.path.join(mOutProjectFolder, "app", "src","main","res","values","colors.xml")
    XmlUtil.writeDocumentxml(colorDocument, colorDocumentPath)

# write to string file
    stringWriter = creator.mWriter
    resourceDocument = stringWriter.mRoot
    stringDocumentPath = os.path.join(mOutProjectFolder, "app", "src","main","res","values","strings.xml")
    XmlUtil.writeDocumentxml(resourceDocument, stringDocumentPath)
    SketchProjectGenerator.prepareProject(projectFolder, projectName)

    return 
