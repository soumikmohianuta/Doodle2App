# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 01:16:09 2019

@author: sxm6202xx
"""
from bs4 import BeautifulSoup
#from ast import literal_eval
from RectUtils.Rect import Rect
from RectUtils.RectObj import RectObj
from RectUtils import RectUtil
#import cssutils
from htmlHelper import HtmlUtil
#htmlFolder = r"C:\Users\sxm6202xx\Desktop\Project\Uploads\screenshotProcessor\templates\newWebItem.html"

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
            print("Coming Here")
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
    for i in range(elementLength-1):
        item=sortedRectObjs[i]
        validElement = True
        isChild = False
#        print(item.rectArea)
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
def jsonToRect(jsonRects):
    rectObjs=[]
    for item in jsonRects:
#        print(item)
        rectObj = RectObj(Rect(int(item['x']),int(item['y']),int(item['width']),int(item['height'])),int(item['iconID']),int(item['elementId']))
        rectObjs.append(rectObj)
    return rectObjs
        

def createHtmlInternally(soup,parElement, rectPar):
    for rectObj in rectPar.mChildren:  
        new_tag = HtmlUtil.newElement(soup, rectObj,rectPar)   
        createHtmlInternally(soup,new_tag, rectObj)
        parElement.append(new_tag)

# generate html
def createHtml(fileName, outFileName,  jsonRootObjs):
    rawRects = jsonToRect(jsonRootObjs)
    file = open(fileName, "r")
    data = file.read()
    soup = BeautifulSoup(data, 'html.parser')
    if(len(rawRects)!=0):
        rootObj = createHierachy(rawRects, 500,600)
        for rectObj in rootObj.mChildren:        
            new_tag = HtmlUtil.newElement(soup, rectObj,rootObj)
            #        print(new_tag)
            createHtmlInternally(soup,new_tag,rectObj)
            soup.body.insert(1,new_tag)
            soup.body.append("")
    with open(outFileName, "w") as file:
            file.write(str(soup))

