##################################
##################################
##     Package necessary
#################################
#################################
#import pandas as pd
import os
import pickle
import json
import numpy as np
##################################
##################################
##     Package for prediction
#################################
#################################
#import the function that introduce your model, fit it with the cleaned data set
from model_ML.Model import model_func
#you put your csv file, you get a cleaned df that is arranged according to the json file by the client
from model_ML.Cleaner_Train_Data import Cleaner_SalesData

##################################
##################################
##     Package for preprocess
#################################
#################################
#pakage to clean the input json file from the client
from Preprocess.Clean import Cleaner_SalesData
from Preprocess.Clean import Processed_JSON


##################################
##################################
##  Package for Flask to take a file from folder, and uploaded (put it) in the website
# I copied this upload file section from flask documentation
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
#we will load the file from asset, and put it in the website
#################################
#################################
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify


# I copied this upload file section from flask documentation
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
app = Flask("__name__")
port = int(os.environ.get("PORT", 5000))


#the first page
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # if it is post, you route it to "/prediction"
        return redirect(url_for('predict_page'))
    else:
        #at the begining, I have get only
        return render_template('index.html') #, error_message=error_message -> error_message_comming_from.preprocessing.preprocess())


# @app.route('/predict/<uuid>', methods=["POST", "GET"])
@app.route('/predict', methods=["POST", "GET"])
def predict_page():
    if request.method == 'POST':
        #json_file = request.json
        json_file=request.get_json()
        #print(json_file)

        #I will create a new dic, that I will pass it to my process
        c_dic = {}
        dict_new = json_file["0"]
        for k, v in dict_new.items():
            if k not in c_dic:
                c_dic[k] = v
        #print(c_dic)
        # # input=json_file
        # preprocessed_dict = Cleaner_SalesData(c_dic)
        # r = preprocessed_dict.cleaning_feature()

        testing_features = Processed_JSON(c_dic)

        modele = pickle.load(open('./asset/model.pkl', 'rb'))
        y_pred_new = (modele.predict([testing_features]))[0]
        y_pred_new =np.round(y_pred_new, 4)
        return jsonify({"prediction": y_pred_new})
    else:
        return jsonify({"prediction": "there is no prediction, no input json file"})

if __name__=="__main__":
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=port)
    #input={'0': {'area': 30, 'property-type': 'APARTMENT', 'rooms-number': 2, 'zip-code': 1050, 'land-area': 200, 'garden': True, 'garden-area': 1}}
    #
    # preprocessed_dict = Cleaner_SalesData(input)
    # r=preprocessed_dict.cleaning_feature()
    # print(r)
    # testing_features = Processed_JSON(input)
    # print(testing_features)
    # modele = pickle.load(open('./asset/model.pkl', 'rb'))
    # y_pred_new = (modele.predict([testing_features]))[0]
    # print(y_pred_new)


