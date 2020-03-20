# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 22:43:19 2019

@author: soumi
"""
from bs4 import BeautifulSoup
from RectUtils.RectObj import RectObj



# set attribute for Icon
def styleIconAttribute(top, left,width, height, position="absolute", color = "white"):
    styleDic = {}
    styleDic["background-color"] = color
    styleDic["position"] = position
    styleDic["top"] = str(top)+ "px"
    styleDic["left"] = str(left)+ "px"   
    styleDic["width"] = str(width)+ "px"
    styleDic["height"] = str(height)+ "px"
    styleString= ""
    for key in styleDic:
        styleString += key+": " + styleDic[key] +";"
    return styleString

# set attribute for Container

def styleContainerAttribute(top, left,width, height,position="absolute"):
    styleDic = {}
    styleDic["position"] = position
    styleDic["top"] = str(top)+ "px"
    styleDic["left"] = str(left)+ "px"   
    styleDic["width"] = str(width)+ "px"
    styleDic["height"] = str(height)+ "px"   
    styleDic["border"] = "1px solid #000"
    styleString= ""
    for key in styleDic:
        styleString += key+": " + styleDic[key] +";"
    return styleString

# set attribute for rest of the item

def styleOtherAttribute(top, left,width, height,position="absolute"):
    styleDic = {}
    styleDic["position"] = position
    styleDic["top"] = str(top)+ "px"
    styleDic["left"] = str(left)+ "px"   
    styleDic["width"] = str(width)+ "px"
    styleDic["height"] = str(height)+ "px"   
    styleString= ""
    for key in styleDic:
        styleString += key+": " + styleDic[key] +";"
    return styleString

# set attribute for text item

def styleTextAttribute(top, left,width, height,position="absolute"):
    styleDic = {}
    styleDic["position"] = position
    styleDic["margin-top"] = str(top)+ "px"
    styleDic["left"] = str(left)+ "px"   
    styleDic["width"] = str(width)+ "px"
    styleDic["height"] = str(height)+ "px"   
    styleDic["background-color"] = str("#bfbdb6")
    styleString= ""
    for key in styleDic:
        styleString += key+": " + styleDic[key] +";"
    return styleString
     


# create element from rectobojs    
def newElement(soup, rectObj,parRect):
    elementId = rectObj.elementId
    left = rectObj.x
    top = rectObj.y
    if(rectObj.isContainer()):    
        styleAttr = styleContainerAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('div', id=elementID, style=styleAttr)
        return new_node
     
    elif(rectObj.isText()):
        styleAttr = styleTextAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('p', id=elementID, style=styleAttr)
        new_node.string = "Hello Text"
        return new_node
    
    elif(rectObj.isButtonText()):
        styleAttr = styleOtherAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('Button', id=elementID, style=styleAttr)
        new_node.string = "Button"
        return new_node
 
    elif(rectObj.isSlider()):
        styleAttr = styleOtherAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('input',type="range",min=1,max=100,value=1, id=elementID, style=styleAttr)
        return new_node
            
           
    elif(rectObj.isToogle()):
        styleAttr = styleOtherAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('label', id=elementID, style=styleAttr)
        input_tag_val = soup.new_tag('input', type="checkbox")
        span_tag_val = soup.new_tag('span', **{'class':'slider'})
        new_node.append(input_tag_val)
        new_node.append(span_tag_val)
        return new_node

    
    elif(rectObj.isCheckbox()):
        styleAttr = styleOtherAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('input',type="checkbox", id=elementID, style=styleAttr)
        return new_node

# create 1,2,3,4 dummy dropdown

    elif(rectObj.isDropDown()):
        styleAttr = styleOtherAttribute(top,left, rectObj.width, rectObj.height)
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('select', id=elementID, style=styleAttr)
        button_tag_val1 = soup.new_tag('option', value="1")
        button_tag_val1.append("1")
        button_tag_val2 = soup.new_tag('option', value="2")
        button_tag_val2.append("2")
        button_tag_val3 = soup.new_tag('option', value="3")
        button_tag_val3.append("3")
        button_tag_val4 = soup.new_tag('option', value="4")
        button_tag_val4.append("4")
        new_node.append(button_tag_val1)
        new_node.append(button_tag_val2)
        new_node.append(button_tag_val3)
        new_node.append(button_tag_val4)
        return new_node

    else:
        iconName = rectObj.getIconName()
        styleAttr = styleIconAttribute(top,left,rectObj.width,rectObj.height)
        imgSrc = "../images/"+iconName+".png"
        elementID = "element" + str(elementId)
        new_node = soup.new_tag('button', id=elementID, style=styleAttr)
        styleImgAttr = styleIconAttribute(0,0,rectObj.width-4,rectObj.height-4)
        button_tag_val = soup.new_tag('img',src=imgSrc, style=styleImgAttr )

#        button_tag_val = soup.new_tag('img',src=imgSrc, height=str(rectObj.height)+"px", width=str(rectObj.width)+"px" )
        new_node.append(button_tag_val)
        return new_node
        
        
def clearElements(fileName, outFileName):
    file = open(fileName, "r")
    data = file.read()
#    print (data)
    soup = BeautifulSoup(data, 'html.parser')
    with open(outFileName, "w") as file:
        file.write(str(soup))