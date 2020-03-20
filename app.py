from __future__ import division
from flask import Flask, render_template, request, url_for,send_from_directory,session,redirect,make_response,jsonify
import os
from htmlHelper import HtmlGenerator
from mlModule.Predictor import Predictor
from mlModule.FastPredict import FastPredict
from mlModule import GetPrediction
from androidHelper import sketchProcessing
from helpers import StrokeParse
from RectUtils.RectObj import RectObj
#import timeit
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'templates/uploads')
STYLESHEETS_FOLDER = os.path.join(APP_ROOT, 'templates','stylesheets')
IMAGES_FOLDER = os.path.join(APP_ROOT, 'templates','images')
FONTS_FOLDER = os.path.join(APP_ROOT, 'templates','fonts')
FONTS_AWESOME_CSS_FOLDER = os.path.join(APP_ROOT, 'templates','font-awesome','css')
FONTS_AWESOME_FONTS_FOLDER = os.path.join(APP_ROOT, 'templates','font-awesome','fonts')
SCRIPTS_FOLDER = os.path.join(APP_ROOT, 'templates','javascripts')
UI_IMAGES_FOLDER= os.path.join(APP_ROOT, 'PrimaryScreenShots','PrimaryFocus')
output_directory = os.path.join(APP_ROOT,'compressedOut')
export_dir = os.path.join(APP_ROOT,'compressedOut','tb')
TemplateFolder = os.path.join(APP_ROOT, 'templates')
#TemplateProjectFolder = os.path.join(APP_ROOT, 'templates', 'templateProject')
ProjectGenerateFolder = os.path.join(APP_ROOT, 'templates', 'sketchupload')

PREDICTOR = Predictor(export_dir,output_directory)
FASTPREDICT = FastPredict(PREDICTOR.classifier,PREDICTOR.example_input_fn)
app = Flask(__name__)
app.secret_key = "pix2appSMDrawKey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def rectObjtoJson(rectObj):
    dictObj = {'x':str(rectObj.x), 'y':str(rectObj.y),'width':str(rectObj.width),'height':str(rectObj.height),'iconID':str(rectObj.iconID),'elementId':str(rectObj.elementId)}
    return dictObj

# Navigate to root page
@app.route('/')
def doodle(): 
    session['ELEMENTID'] =  0
    session['RectObjs'] = []
    
    return render_template('homepageFullHTML.html')



# Set the size of the canvas
@app.route('/SetCanvasSize/', methods=['GET','POST'])
def SetCanvasSize(): 
    session['canvas_width'] =  request.form['canvas_size']    
    print(session['canvas_width'])
    return render_template('homepageFullHTML.html')


# send html for rendering
@app.route('/doodle/newWeb')
def send_new_web_Item():
    elementID = session['ELEMENTID']
 
    if(elementID==0):
        return send_from_directory(TemplateFolder, 'checkHtml.html')
    else:
        return send_from_directory(TemplateFolder, 'newWebItem.html')
   
# update html for rendering
@app.route('/newWeb/<filename>')
def send_refresh_web_Item(filename):
    return send_from_directory(TemplateFolder, 'newWebItem.html')

# update html for rendering
@app.route('/newWeb/')
def newWeb():   
#    return render_template('newWebItem.html')
    elementId = session['ELEMENTID']
    if elementId==0:
        return render_template('checkHtml.html')
    else:
        return render_template('newWebItem.html')


# Generate Html Element
def generateHtmlElement():
    elementID = session['ELEMENTID']
    rectObjs = session['RectObjs']
    infile = os.path.join(TemplateFolder, "checkHtml.html")
    outfile =  os.path.join(TemplateFolder, "newWebItem.html")
    HtmlGenerator.createHtml(infile, outfile, rectObjs)
    session['ELEMENTID'] = elementID+1
    return 


@app.route('/RemoveLastIcon/', methods=['GET','POST'])
def RemoveLastIcon():
    elementID = session['ELEMENTID']
    rectObjs = session['RectObjs']
    for item in rectObjs:
        if(item['elementId'] == str(elementID-1)):
            rectObjs.remove(item)
            break
#    print(rectObjs)
    session['RectObjs'] =  rectObjs  
    infile = os.path.join(TemplateFolder, "checkHtml.html")
    outfile =  os.path.join(TemplateFolder, "newWebItem.html")
    HtmlGenerator.createHtml(infile, outfile, rectObjs)
    session['ELEMENTID'] = elementID-1
    return "Success"
    

# Predict midway of drawing
@app.route('/MidPredict/', methods=['GET','POST'])
def MidPredict():
    if request.method == 'POST':
        canvas_strokes = request.form['save_data']

        compressStroke,rect = StrokeParse.compressDataForFullUI(canvas_strokes)
        print(rect.x,rect.y, rect.width+rect.x, rect.height+rect.y)

        if len(compressStroke)==0:
            result = "Unchanged" 
        else:
            result, resultID =GetPrediction.getFasterPredictResultForFullUI(compressStroke, PREDICTOR, FASTPREDICT )
        response = jsonify(predictedResult =result)
        return response




@app.route('/DrawSave/', methods=['GET','POST'])
def DrawSave():
    elementID = session['ELEMENTID']
    if request.method == 'POST':
        canvas_strokes = request.form['save_data']
#        print(canvas_strokes)

        compressStroke,rect = StrokeParse.compressDataForFullUI(canvas_strokes)
        if len(compressStroke)==0:
            result = "Unchanged" 
        else:
            result, resultID = GetPrediction.getFasterPredictResultForFullUI(compressStroke, PREDICTOR, FASTPREDICT )
            rectObj = RectObj(rect,resultID,elementID)
            jsonRectObj = rectObjtoJson(rectObj)
#            print(rectObj)
            jsonRectObjs = session['RectObjs']
            
            jsonRectObjs.append(jsonRectObj)
            session['RectObjs'] = jsonRectObjs
 
            generateHtmlElement()
        response = jsonify(predictedResult =result)
        return response

@app.route('/Predict/', methods=['GET','POST'])
def Predict():
    if request.method == 'POST':
        canvas_strokes = request.form['save_data']
        compressStroke = StrokeParse.compressData(canvas_strokes)
        result =GetPrediction.getFasterPredictResult(compressStroke, PREDICTOR, FASTPREDICT )
        response = jsonify(predictedResult =result)
        return response
    



def generateAndroid():
    elementID = session['ELEMENTID']
    rectObjs = session['RectObjs']
    if len(rectObjs)==0:
        return 
    sketchProcessing.generateProject(rectObjs,ProjectGenerateFolder,TemplateFolder,int(session['canvas_width'])  )

    session['ELEMENTID'] = elementID+1
    return 

@app.route('/sketchAndroidCode/', methods=['GET','POST'])
def sketchAndroidCode():

#        start = timeit.default_timer()
        generateAndroid()
#        stop = timeit.default_timer()
#        print('Code Generation Time: ', stop - start)  
        projectName = "SketchToUI"
#        projectLocation = os.path.join(ProjectGenerateFolder, projectName+".zip")
        projectLocation = "/sketchupload/" +projectName+".zip"
#        return render_template('consent.html')
        return render_template('project.html', name_of_file = projectName, image_path= projectLocation)
     

    
 
    

@app.route('/DoodleHeaderText/', methods=['GET','POST'])
def DoodleHeaderText():
    curCateogry = 0
    if 'doodleHeader' in session:
        session['doodleHeader'] =  (int(session['doodleHeader'])+1)%21
        curCateogry = int(session['doodleHeader'])
    else:
        session['doodleHeader'] =  0
    category =['Text (Squiggle line)',' Text Button (container around squiggle line)','Switch (a toggle element)',' Slider','Checkbox','Back','Menu (the Hamburger)','Cancel (Close)','Search (Loupe)','Plus (Add)','Avatar (User Image)','Share','Settings (Gear)','Settings','Forward','Play','Left-Arrow','Container (Square)','Dropdown','Envelop','Camera']
    
    cText = category[curCateogry]
    response = jsonify(hText = cText)
    return response
    


#        return render_template('generated-project.html', is_it_plagiarized=is_it_plagiarized, checkImage= sfname)
@app.route('/sketchupload/<filename>')
def send_zip_file(filename):
    return send_from_directory(ProjectGenerateFolder, filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/stylesheets/<filename>')
def send_css(filename):
    return send_from_directory(STYLESHEETS_FOLDER, filename)

@app.route('/images/<filename>')
def send_img(filename):
    return send_from_directory(IMAGES_FOLDER, filename)

@app.route('/fonts/<filename>')
def send_fonts(filename):
    return send_from_directory(FONTS_FOLDER, filename)

@app.route('/font-awesome/css/<filename>')
def send_fontawscss(filename):
    return send_from_directory(FONTS_AWESOME_CSS_FOLDER, filename)

@app.route('/font-awesome/fonts/<filename>')
def send_fontawsfont(filename):
    return send_from_directory(FONTS_AWESOME_FONTS_FOLDER, filename)
    

@app.route('/CurentImage/<filename>')
def send_interval_img(filename):


    curDrawingName=  session['current_element']+ ".png"
      
    return send_from_directory(UI_IMAGES_FOLDER, curDrawingName)

 
    
@app.route('/javascripts/<filename>')
def send_jss(filename):
    return send_from_directory(SCRIPTS_FOLDER, filename)

@app.route('/doodle/images/<filename>')
def send_fullUI_img(filename):
    return send_from_directory(IMAGES_FOLDER, filename)
if __name__ == "__main__":
    
    app.run(threaded=True)
