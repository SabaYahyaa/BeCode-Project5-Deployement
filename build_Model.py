"""
This file gives a pickle file that stores you model in asset
Later we call the model, we input a json file to it, to get the prediction
"""

#import the function that introduce your model, fit it with the cleaned data set
from model_ML.Model import model_func
#you put your csv file, you get a cleaned df that is arranged according to the json file by the client
from model_ML.Cleaner_Train_Data import Cleaner_SalesData

# Reading the csv (our data)
url = 'https://raw.githubusercontent.com/FrancescoMariottini/project3/main/inputs/all_sales_data.csv'
#create an instance of a class that cean our data and prepare data as the coming from client
ss = Cleaner_SalesData(url)
#gets the cleaned daa in a df formet
df_cleaned = ss.cleaning_feature()
print(df_cleaned.columns.tolist())
## 1. Train the model
df_to_ML_model=df_cleaned[['zip-code','area','rooms-number','garden', 'garden-area','terrace', 'terrace-area','land-area','open-fire',
                           'swimmingpool','equipped-kitchen','furnished','facades-number', 'property-type_APARTMENT', 'property-type_HOUSE', 'property-type_OTHERS', 'building-state_NEW', 'building-state_GOOD', 'building-state_TO RENOVATE', 'building-state_JUST RENOVATED', 'building-state_TO REBUILD', 'price']]

#train your mode, and store it in a pickle file, the picle file will be stored under asset
model_func(df_to_ML_model)

print("your model (model.pickle) is built under the asset folder")














# from flask import Flask, render_template, flash, request, redirect, url_for
# from werkzeug import secure_filename
# from preprocessing import preprocess
# from model import model_func
# from predict import predict
# import pandas as pd
# import os
#
# # '/path/to/the/uploads' | os.getcwd() == current directory
# UPLOAD_FOLDER = os.getcwd()+'/Datasets'
# ALLOWED_EXTENSIONS = {'json'}
#
# # I copied this upload file section from flask documentation
# # https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
# app = Flask("__name__")
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# @app.route('/', methods=["POST", "GET"])
# def index():
#     if request.method == "POST":
#         # if it is post, you route it to "/prediction"
#         return redirect(url_for('predict_page'))
#     else:
#         return render_template('index.html') #, error_message=error_message -> error_message_comming_from.preprocessing.preprocess())
#
# # toallow only json file
# def allowed_file(filename):
#     return '.' in filename and \
#        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# # @app.route('/predict/<uuid>', methods=["POST", "GET"])
# @app.route('/predict', methods=["POST", "GET"])
# def predict_page():
#     # content = request.get_json()
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#         # we saved new json file inside Datasets folder.
#         # Now, we call it with process function and then we pass it through our model.
#             cleaned_json_df = preprocess(file.filename)
#             model = model_func()
#             y_pred_new = predict(cleaned_json_df, model)
#             y_pred_new = str(y_pred_new)
#
#             return render_template("predict.html", price_predicted=y_pred_new )
#     else:
#         return '''
#                 <html>
#                     <body>
#                         <form enctype = "multipart/form-data" method = "post">
#                             <p>Upload File: <input type = "file" name = "file" />
#                             <p><input type = "submit" value = "Upload" /></p>
#                         </form>
#                     </body>
#                 </html>
#                 '''
#
# if __name__ == "__main__":
#     app.run(debug=True)