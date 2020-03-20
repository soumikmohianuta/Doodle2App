# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 02:11:47 2018

@author: soumi
"""

from Utils import Util
from Utils import XmlUtil
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse
from Utils import Constants
import zipfile
import os
debugMode = True

#TEMPLATE_FOLDER = r"templates\\"
# clear content of the generated project folder

def clearContent(projectPath):
    Util.run("rm -rf"+ projectPath+ "*")



# copy the template project     
def createProject(projectFolder, templateFolder):
#    fartPath = os.path.join(templateFolder, "fart.exe")
    templateProjectPath = os.path.join(templateFolder,"SketchToUI" )
#    Util.run("mkdir " +projectFolder)
#    Util.run("Xcopy /E /I " +templateProjectPath +" "+ projectFolder)
    Util.run("cp -a " +templateProjectPath +" "+ projectFolder)
    

def setup(projectFolder , templateFolder):
    project = os.path.join(projectFolder,"SketchToUI" )
    if(os.path.exists(project)):
        Util.run("rm -rf " + projectFolder+"/*")
    createProject(projectFolder, templateFolder)

    
    
def projectCompile(projectInfo):

    Util.run(projectInfo.mPath +"//gradlew assembleDebug" )
        


# prepare project for download
def prepareProject(projectPath, projectName):

    zipFileName = os.path.join( projectPath, projectName+".zip")
    mprojectPath = os.path.join( projectPath, projectName)
    zipdirectory(mprojectPath,zipFileName )


# create zip of the created folder
def zipdirectory(basedir, archivename):
    zf = zipfile.ZipFile(archivename, "w", zipfile.ZIP_DEFLATED)
    Util.run("chmod -R 777 "+archivename )

    for root, dirs, files in os.walk(basedir):
           #NOTE: ignore empty directories
           for fn in files:
               absfn = os.path.join(root, fn)
               zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
               zf.write(absfn,zfn)
    zf.close()	

    Util.run("chmod -R 777 "+archivename )


