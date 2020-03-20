from helpers import UploadS3,UploadS3Turk



def storeElement(currentElement,elementCounts):

    if currentElement in elementCounts:
        elementCounts[currentElement]= elementCounts[currentElement]+1
    else:
        elementCounts[currentElement] = 1
    count = elementCounts[currentElement]
       
    return currentElement + '_'+ str(count)



def storeElementToS3(currentElement, fileName):
        UploadS3.upload_file_to_s3(currentElement,fileName)

def storeTurkElementToS3(currentElement, fileName):
        UploadS3Turk.upload_file_to_s3(currentElement,fileName)
        
        
def storeElementsToS3(currentElements):
    print("Dear oh Dear")
#    for element in currentElements:  
#        UploadS3.upload_file_to_s3(element,currentElements[element])
