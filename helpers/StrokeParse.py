import json
from RectUtils.Rect import Rect
from ast import literal_eval
#        
def removeDuplicates(strokes):
    newStrokes=[]
    for stroke in strokes:
        newstroke= []
        newXPoints = []
        newYPoints = []
        xPoints = stroke[0]
        yPoints = stroke[1]
        pointCount = len(xPoints)
        for i in range(pointCount-1):
            if(xPoints[i]==xPoints[i+1] and yPoints[i]==yPoints[i+1]):
                continue
            else:
                newXPoints.append(xPoints[i+1])
                newYPoints.append(yPoints[i+1])
        newstroke.append(newXPoints)
        newstroke.append(newYPoints)
        newStrokes.append(newstroke)
    return newStrokes    

def compressData(content): 
    parsed_json = json.loads(content)
    strokes = []
    strokeSize=[]
    for singleStroke in parsed_json:
        lines = singleStroke["lines"]
        strokeSize.append(singleStroke["size"])
        stroke = []
        xLine=[]
        yLine=[]
        for line in lines:
            startPoint = line['start']
            endPoint = line['end']
            xLine.append(int(startPoint['x']))
            xLine.append(int(endPoint['x']))
            yLine.append(int(startPoint['y']))
            yLine.append(int(endPoint['y']))
        stroke.append(xLine)
        stroke.append(yLine)
        strokes.append(stroke)
#    strokes.append(strokeSize)
    return strokes     


def compressAllData(content):  
#    parsed_json = json.loads(content)
    content = literal_eval(content)
    strokeStack = []
    for single_parse in content:
#        print(single_parse)
#        parsed_json = json.loads(str(single_parse))
        strokes = []
        jsonStrokes = single_parse["stroke"]
        for singleStroke in jsonStrokes:
            lines = singleStroke["lines"]
#            strokeSize.append(singleStroke["size"])
            stroke = []
            xLine=[]
            yLine=[]
            for line in lines:
                startPoint = line['start']
                endPoint = line['end']
                xLine.append(int(startPoint['x']))
                xLine.append(int(endPoint['x']))
                yLine.append(int(startPoint['y']))
                yLine.append(int(endPoint['y']))
            stroke.append(xLine)
            stroke.append(yLine)
            strokes.append(stroke)
#    strokes.append(strokeSize)

        comrpessStore = removeDuplicates(strokes)
        strokeStack.append(comrpessStore)
#    strokes.append(strokeSize)
    return strokeStack     
            
def compressDataFromFile(directory, file):
    with open('starButton_1' ) as f:
        elmtList = f.read()    
    parsed_json = json.loads(elmtList)
    strokes = []
    strokeSize=[]
    for singleStroke in parsed_json:
        lines = singleStroke["lines"]
        strokeSize.append(singleStroke["size"])
        stroke = []
        xLine=[]
        yLine=[]
        for line in lines:
            startPoint = line['start']
            endPoint = line['end']
            xLine.append(startPoint['x'])
            xLine.append(endPoint['x'])
            yLine.append(startPoint['y'])
            yLine.append(endPoint['y'])
        stroke.append(xLine)
        stroke.append(yLine)
        strokes.append(stroke)

#    strokes.append(strokeSize)    
    return strokes
        
            
def compressDataForFullUI(content):    
    parsed_json = json.loads(content)
    strokes = []
    strokeSize=[]
    xLines= []
    yLines=[]
    if len(parsed_json) == 0:
            rect = Rect( 0,0,0,0   )
            return (strokes,rect)  

    for singleStroke in parsed_json:
        lines = singleStroke["lines"]
        strokeSize.append(singleStroke["size"])
        stroke = []
        xLine=[]
        yLine=[]
        for line in lines:
            startPoint = line['start']
            endPoint = line['end']
            xLine.append(int(startPoint['x']))
            xLine.append(int(endPoint['x']))
            yLine.append(int(startPoint['y']))
            yLine.append(int(endPoint['y']))
            
        stroke.append(xLine)
        stroke.append(yLine)
        strokes.append(stroke)
        xLines.extend(xLine)
        yLines.extend(yLine)
    xLines.sort()
    yLines.sort()
    x = xLines[0]
    y= yLines[0]
    width = xLines[-1] - xLines[0]
    height = yLines[-1] - yLines[0]
    rect = Rect( x,y,width,height   )
    
#    strokes.append(strokeSize)
    return (strokes,rect)     


#if __name__ == "__main__":
#    with open('starButton_1' ) as f:
#        elmtList = f.read()
#    strokes = compressData(elmtList)
#    print(strokes)
#    img = strokeToSquareImage(strokes)
#    showStrokeImage(img)

#A = [{"stroke":[{"color":"#000000","size":5,"lines":[{"start":{"x":47.625,"y":47.2734375},"end":{"x":53.625,"y":47.2734375}},{"start":{"x":53.625,"y":47.2734375},"end":{"x":56.625,"y":47.2734375}},{"start":{"x":56.625,"y":47.2734375},"end":{"x":57.625,"y":47.2734375}},{"start":{"x":57.625,"y":47.2734375},"end":{"x":65.625,"y":47.2734375}},{"start":{"x":65.625,"y":47.2734375},"end":{"x":73.625,"y":47.2734375}},{"start":{"x":73.625,"y":47.2734375},"end":{"x":76.625,"y":47.2734375}},{"start":{"x":76.625,"y":47.2734375},"end":{"x":85.625,"y":47.2734375}},{"start":{"x":85.625,"y":47.2734375},"end":{"x":91.625,"y":47.2734375}},{"start":{"x":91.625,"y":47.2734375},"end":{"x":100.625,"y":48.2734375}},{"start":{"x":100.625,"y":48.2734375},"end":{"x":105.625,"y":48.2734375}},{"start":{"x":105.625,"y":48.2734375},"end":{"x":125.625,"y":48.2734375}},{"start":{"x":125.625,"y":48.2734375},"end":{"x":127.625,"y":48.2734375}},{"start":{"x":127.625,"y":48.2734375},"end":{"x":131.625,"y":48.2734375}}]},{"color":"#000000","size":5,"lines":[{"start":{"x":40.625,"y":82.2734375},"end":{"x":40.625,"y":83.2734375}},{"start":{"x":40.625,"y":83.2734375},"end":{"x":45.625,"y":83.2734375}},{"start":{"x":45.625,"y":83.2734375},"end":{"x":53.625,"y":83.2734375}},{"start":{"x":53.625,"y":83.2734375},"end":{"x":62.625,"y":83.2734375}},{"start":{"x":62.625,"y":83.2734375},"end":{"x":73.625,"y":83.2734375}},{"start":{"x":73.625,"y":83.2734375},"end":{"x":77.625,"y":83.2734375}},{"start":{"x":77.625,"y":83.2734375},"end":{"x":87.625,"y":83.2734375}},{"start":{"x":87.625,"y":83.2734375},"end":{"x":97.625,"y":83.2734375}},{"start":{"x":97.625,"y":83.2734375},"end":{"x":100.625,"y":83.2734375}},{"start":{"x":100.625,"y":83.2734375},"end":{"x":111.625,"y":83.2734375}},{"start":{"x":111.625,"y":83.2734375},"end":{"x":120.625,"y":83.2734375}},{"start":{"x":120.625,"y":83.2734375},"end":{"x":135.625,"y":83.2734375}}]},{"color":"#000000","size":5,"lines":[{"start":{"x":27.625,"y":130.2734375},"end":{"x":36.625,"y":131.2734375}},{"start":{"x":36.625,"y":131.2734375},"end":{"x":57.625,"y":131.2734375}},{"start":{"x":57.625,"y":131.2734375},"end":{"x":77.625,"y":131.2734375}},{"start":{"x":77.625,"y":131.2734375},"end":{"x":107.625,"y":131.2734375}},{"start":{"x":107.625,"y":131.2734375},"end":{"x":137.625,"y":131.2734375}},{"start":{"x":137.625,"y":131.2734375},"end":{"x":170.625,"y":131.2734375}},{"start":{"x":170.625,"y":131.2734375},"end":{"x":207.625,"y":131.2734375}},{"start":{"x":207.625,"y":131.2734375},"end":{"x":245.625,"y":131.2734375}},{"start":{"x":245.625,"y":131.2734375},"end":{"x":277.625,"y":131.2734375}},{"start":{"x":277.625,"y":131.2734375},"end":{"x":310.625,"y":131.2734375}},{"start":{"x":310.625,"y":131.2734375},"end":{"x":332.625,"y":131.2734375}},{"start":{"x":332.625,"y":131.2734375},"end":{"x":340.625,"y":131.2734375}}]}]},{"stroke":[{"color":"#000000","size":5,"lines":[{"start":{"x":182.625,"y":411.2734375},"end":{"x":188.625,"y":411.2734375}},{"start":{"x":188.625,"y":411.2734375},"end":{"x":197.625,"y":411.2734375}},{"start":{"x":197.625,"y":411.2734375},"end":{"x":210.625,"y":411.2734375}},{"start":{"x":210.625,"y":411.2734375},"end":{"x":217.625,"y":411.2734375}},{"start":{"x":217.625,"y":411.2734375},"end":{"x":232.625,"y":411.2734375}},{"start":{"x":232.625,"y":411.2734375},"end":{"x":250.625,"y":410.2734375}},{"start":{"x":250.625,"y":410.2734375},"end":{"x":267.625,"y":410.2734375}},{"start":{"x":267.625,"y":410.2734375},"end":{"x":281.625,"y":408.2734375}},{"start":{"x":281.625,"y":408.2734375},"end":{"x":290.625,"y":408.2734375}},{"start":{"x":290.625,"y":408.2734375},"end":{"x":302.625,"y":407.2734375}},{"start":{"x":302.625,"y":407.2734375},"end":{"x":310.625,"y":407.2734375}},{"start":{"x":310.625,"y":407.2734375},"end":{"x":312.625,"y":407.2734375}}]},{"color":"#000000","size":5,"lines":[{"start":{"x":247.625,"y":361.2734375},"end":{"x":247.625,"y":366.2734375}},{"start":{"x":247.625,"y":366.2734375},"end":{"x":247.625,"y":377.2734375}},{"start":{"x":247.625,"y":377.2734375},"end":{"x":247.625,"y":385.2734375}},{"start":{"x":247.625,"y":385.2734375},"end":{"x":247.625,"y":396.2734375}},{"start":{"x":247.625,"y":396.2734375},"end":{"x":247.625,"y":408.2734375}},{"start":{"x":247.625,"y":408.2734375},"end":{"x":247.625,"y":418.2734375}},{"start":{"x":247.625,"y":418.2734375},"end":{"x":247.625,"y":431.2734375}},{"start":{"x":247.625,"y":431.2734375},"end":{"x":247.625,"y":440.2734375}},{"start":{"x":247.625,"y":440.2734375},"end":{"x":250.625,"y":447.2734375}},{"start":{"x":250.625,"y":447.2734375},"end":{"x":252.625,"y":458.2734375}},{"start":{"x":252.625,"y":458.2734375},"end":{"x":255.625,"y":461.2734375}},{"start":{"x":255.625,"y":461.2734375},"end":{"x":255.625,"y":463.2734375}},{"start":{"x":255.625,"y":463.2734375},"end":{"x":263.625,"y":470.2734375}},{"start":{"x":263.625,"y":470.2734375},"end":{"x":265.625,"y":476.2734375}},{"start":{"x":265.625,"y":476.2734375},"end":{"x":270.625,"y":477.2734375}}]},{"color":"#000000","size":5,"lines":[{"start":{"x":302.625,"y":372.2734375},"end":{"x":301.625,"y":371.2734375}}]},{"color":"#000000","size":5,"lines":[{"start":{"x":295.625,"y":365.2734375},"end":{"x":290.625,"y":360.2734375}},{"start":{"x":290.625,"y":360.2734375},"end":{"x":285.625,"y":356.2734375}},{"start":{"x":285.625,"y":356.2734375},"end":{"x":282.625,"y":353.2734375}},{"start":{"x":282.625,"y":353.2734375},"end":{"x":282.625,"y":351.2734375}},{"start":{"x":282.625,"y":351.2734375},"end":{"x":281.625,"y":351.2734375}},{"start":{"x":281.625,"y":351.2734375},"end":{"x":277.625,"y":351.2734375}},{"start":{"x":277.625,"y":351.2734375},"end":{"x":275.625,"y":351.2734375}},{"start":{"x":275.625,"y":351.2734375},"end":{"x":275.625,"y":350.2734375}},{"start":{"x":275.625,"y":350.2734375},"end":{"x":267.625,"y":350.2734375}},{"start":{"x":267.625,"y":350.2734375},"end":{"x":263.625,"y":347.2734375}},{"start":{"x":263.625,"y":347.2734375},"end":{"x":261.625,"y":347.2734375}},{"start":{"x":261.625,"y":347.2734375},"end":{"x":252.625,"y":347.2734375}},{"start":{"x":252.625,"y":347.2734375},"end":{"x":247.625,"y":347.2734375}},{"start":{"x":247.625,"y":347.2734375},"end":{"x":237.625,"y":347.2734375}},{"start":{"x":237.625,"y":347.2734375},"end":{"x":206.625,"y":353.2734375}},{"start":{"x":206.625,"y":353.2734375},"end":{"x":195.625,"y":358.2734375}},{"start":{"x":195.625,"y":358.2734375},"end":{"x":180.625,"y":367.2734375}},{"start":{"x":180.625,"y":367.2734375},"end":{"x":172.625,"y":371.2734375}},{"start":{"x":172.625,"y":371.2734375},"end":{"x":168.625,"y":372.2734375}},{"start":{"x":168.625,"y":372.2734375},"end":{"x":157.625,"y":380.2734375}},{"start":{"x":157.625,"y":380.2734375},"end":{"x":157.625,"y":381.2734375}},{"start":{"x":157.625,"y":381.2734375},"end":{"x":157.625,"y":388.2734375}},{"start":{"x":157.625,"y":388.2734375},"end":{"x":157.625,"y":401.2734375}},{"start":{"x":157.625,"y":401.2734375},"end":{"x":157.625,"y":407.2734375}},{"start":{"x":157.625,"y":407.2734375},"end":{"x":160.625,"y":410.2734375}},{"start":{"x":160.625,"y":410.2734375},"end":{"x":165.625,"y":413.2734375}},{"start":{"x":165.625,"y":413.2734375},"end":{"x":170.625,"y":427.2734375}},{"start":{"x":170.625,"y":427.2734375},"end":{"x":182.625,"y":452.2734375}},{"start":{"x":182.625,"y":452.2734375},"end":{"x":192.625,"y":457.2734375}},{"start":{"x":192.625,"y":457.2734375},"end":{"x":192.625,"y":460.2734375}},{"start":{"x":192.625,"y":460.2734375},"end":{"x":195.625,"y":460.2734375}},{"start":{"x":195.625,"y":460.2734375},"end":{"x":206.625,"y":466.2734375}},{"start":{"x":206.625,"y":466.2734375},"end":{"x":217.625,"y":475.2734375}},{"start":{"x":217.625,"y":475.2734375},"end":{"x":226.625,"y":478.2734375}},{"start":{"x":226.625,"y":478.2734375},"end":{"x":232.625,"y":480.2734375}},{"start":{"x":232.625,"y":480.2734375},"end":{"x":235.625,"y":480.2734375}},{"start":{"x":235.625,"y":480.2734375},"end":{"x":240.625,"y":481.2734375}},{"start":{"x":240.625,"y":481.2734375},"end":{"x":243.625,"y":481.2734375}},{"start":{"x":243.625,"y":481.2734375},"end":{"x":247.625,"y":481.2734375}},{"start":{"x":247.625,"y":481.2734375},"end":{"x":250.625,"y":481.2734375}},{"start":{"x":250.625,"y":481.2734375},"end":{"x":255.625,"y":481.2734375}},{"start":{"x":255.625,"y":481.2734375},"end":{"x":257.625,"y":480.2734375}},{"start":{"x":257.625,"y":480.2734375},"end":{"x":261.625,"y":480.2734375}},{"start":{"x":261.625,"y":480.2734375},"end":{"x":267.625,"y":476.2734375}},{"start":{"x":267.625,"y":476.2734375},"end":{"x":270.625,"y":475.2734375}},{"start":{"x":270.625,"y":475.2734375},"end":{"x":275.625,"y":472.2734375}},{"start":{"x":275.625,"y":472.2734375},"end":{"x":281.625,"y":468.2734375}},{"start":{"x":281.625,"y":468.2734375},"end":{"x":292.625,"y":455.2734375}},{"start":{"x":292.625,"y":455.2734375},"end":{"x":295.625,"y":450.2734375}},{"start":{"x":295.625,"y":450.2734375},"end":{"x":302.625,"y":446.2734375}},{"start":{"x":302.625,"y":446.2734375},"end":{"x":305.625,"y":441.2734375}},{"start":{"x":305.625,"y":441.2734375},"end":{"x":307.625,"y":435.2734375}},{"start":{"x":307.625,"y":435.2734375},"end":{"x":320.625,"y":412.2734375}},{"start":{"x":320.625,"y":412.2734375},"end":{"x":322.625,"y":407.2734375}},{"start":{"x":322.625,"y":407.2734375},"end":{"x":322.625,"y":405.2734375}},{"start":{"x":322.625,"y":405.2734375},"end":{"x":322.625,"y":402.2734375}},{"start":{"x":322.625,"y":402.2734375},"end":{"x":322.625,"y":396.2734375}},{"start":{"x":322.625,"y":396.2734375},"end":{"x":322.625,"y":385.2734375}},{"start":{"x":322.625,"y":385.2734375},"end":{"x":322.625,"y":380.2734375}},{"start":{"x":322.625,"y":380.2734375},"end":{"x":315.625,"y":371.2734375}},{"start":{"x":315.625,"y":371.2734375},"end":{"x":312.625,"y":367.2734375}},{"start":{"x":312.625,"y":367.2734375},"end":{"x":307.625,"y":365.2734375}},{"start":{"x":307.625,"y":365.2734375},"end":{"x":292.625,"y":362.2734375}},{"start":{"x":292.625,"y":362.2734375},"end":{"x":287.625,"y":362.2734375}},{"start":{"x":287.625,"y":362.2734375},"end":{"x":282.625,"y":361.2734375}},{"start":{"x":282.625,"y":361.2734375},"end":{"x":277.625,"y":360.2734375}},{"start":{"x":277.625,"y":360.2734375},"end":{"x":275.625,"y":360.2734375}},{"start":{"x":275.625,"y":360.2734375},"end":{"x":267.625,"y":357.2734375}},{"start":{"x":267.625,"y":357.2734375},"end":{"x":265.625,"y":357.2734375}}]}]}]
##json.loads(str(A))
#print(compressAllData(A))