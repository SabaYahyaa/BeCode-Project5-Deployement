##################################
##################################
##     Package necessary
#################################
#################################
import pandas as pd
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
from flask import Flask, render_template, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


# '/path/to/the/uploads' | os.getcwd() == current directory
UPLOAD_FOLDER = os.getcwd()+'/asset'
ALLOWED_EXTENSIONS = {'json'}  #accept only json file


# I copied this upload file section from flask documentation
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
app = Flask("__name__")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
App_ROOT=os.path.dirname(os.path.abspath(__file__))

#the first page
@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # if it is post, you route it to "/prediction"
        return redirect(url_for('predict_page'))
    else:
        #at the begining, I have get only
        return render_template('index.html') #, error_message=error_message -> error_message_comming_from.preprocessing.preprocess())

#If the predict page, we will have 2 button predict, and load
#we need to allow only json file, this is from the Flask documentation
def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/predict/<uuid>', methods=["POST", "GET"])
@app.route('/predict', methods=["POST", "GET"])
def predict_page():
    f=" "
    target=os.path.join(App_ROOT, 'asset/')
    print(target)
    if request.method == 'POST':

        file = request.files['file']
        f=file.filename
        print("hhhhhhhhere")
        print(f)
    # #get the path, where you should put your json file
    # client_json = os.path.join(target, f)
    # # # get the prediction
    modele = pickle.load(open('./asset/model.pkl', 'rb'))
    # #get X_test
    testing_features = Processed_JSON(client_json)
    y_pred_new = (modele.predict([testing_features]))[0]

    #print(f"y_pred_new={y_pred_new}")
    return render_template("predict_S.html")


    # #we loaded the file to the user from our laptop,
    # # this will only mention the input
    # testing_features = Processed_JSON("./asset/input_data.json")
    # # get the prediction
    # modele = pickle.load(open('./asset/model.pkl', 'rb'))
    # y_pred_new = (modele.predict([testing_features]))[0]
    #
    # ss = Cleaner_SalesData("./asset/input_data.json")
    # new_json_df = ss.cleaning_feature()
    #
    # #return render_template("predict.html",price_predicted=y_pred_new)
    # return render_template("predict.html", original_json_df=new_json_df, len=len(y_pred_new),
    #                                price_predicted=y_pred_new)



if __name__=="__main__":
    app.run(debug=True)








#
#
#
# #this will only mention the input
# testing_features=Processed_JSON("./asset/input_data.json")
#
# #get the prediction
# modele=pickle.load(open('./asset/model.pkl','rb'))
# y_pred_new = (modele.predict([testing_features]))
#
#
#
# #testing_features = Processed_JSON(url_json)
# print(testing_features)
# print(y_pred_new[0])