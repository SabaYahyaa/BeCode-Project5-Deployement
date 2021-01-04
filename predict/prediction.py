"""
Get the json input, processed it under te Preprocessing folder,
then get the prediction of the model

"""
import numpy as np
import pickle
from Preprocess import  Processed_JSON
def predict(X_test):
    modele = pickle.load(open('asset/model.pkl', 'rb'))
    y_pred_new = (modele.predict([X_test]))
    return (y_pred_new)

if __name__=="__main__":
    #take the input json
    url_json = 'Project5-Api_deployment/asset/input_data.json'
    #clean it using the Preprocess.py
    x_test=Processed_JSON(url_json)
    #get the prediction
    pre=predict(x_test)


# modele=pickle.load(open('asset/model.pkl','rb'))
# y_pred_new = np.array2string(modele.predict(X_new_json))
    #return y_pred_new
#down load the pickel file that stores, the model
#modele = pickle.load(open('/Datasets/model.pkl','rb'))
#read the prediction

#url_json='Datasets/'+str(new_json_name)
