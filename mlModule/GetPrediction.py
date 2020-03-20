from helpers import StrokeParse
class_names= ['back','camera','cancel','checkbox','dropDown','envelope','forward','hamburger','leftarrow','play','plus','search','settings',
               'share','sliders','square','star','text','toogle','userImage']

def getFasterPredictResultForFullUI(redundata, PREDICTOR, FASTPREDICT ):
    data = StrokeParse.removeDuplicates(redundata)
    features1 = PREDICTOR.parse_features(str(data))
    predict_results = FASTPREDICT.predict(features1)
    for idx, prediction in enumerate(predict_results):
          index = prediction["classes"]  # Get the predicted class (index)
          probability = prediction["probabilities"][index]
          result = class_names[index]
#          result = class_names[index]
#          print(probability)
          result = result + " with probability "+ str(probability)

    return result,index+1


def getFasterPredictResult(redundata, PREDICTOR, FASTPREDICT ):
    if(len(redundata)==0):
        return "Start Drawing"
    data = StrokeParse.removeDuplicates(redundata)
    features1 = PREDICTOR.parse_features(str(data))
    predict_results = FASTPREDICT.predict(features1)
    for idx, prediction in enumerate(predict_results):
          index = prediction["classes"]  # Get the predicted class (index)
          probability = prediction["probabilities"][index]
          probability = "{0:.2f}".format(probability*100)
          className = class_names[index]
          result = "Predicted  <strong>" + className + "</strong> with probability :" + str(probability) 

    return result