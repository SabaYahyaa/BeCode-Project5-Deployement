#I want to create a mongo data base, import df to mpongodb
# Step 1: Import the necessary libraries
import quandl
import pandas as pd
import pymongo
from pymongo import MongoClient


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
df_to_ML_model=df_cleaned[['zip-code','area','rooms-number','garden', 'garden-area','terrace', 'terrace-area',
                           'land-area','open-fire','swimmingpool','equipped-kitchen','furnished','facades-number',
                           'property-type_APARTMENT', 'property-type_HOUSE', 'property-type_OTHERS', 'building-state_NEW',
                           'building-state_GOOD', 'building-state_TO RENOVATE', 'building-state_JUST RENOVATED',
                           'building-state_TO REBUILD', 'price']]


##############################
##############################
######## Since, we get an error when we send our df to mongodb because it has large number of rows
######## I will create 3 collections that are not connected. Two of my collection,
# I will store my data in and the 3rd one to store new sample that is scrapped
##############################
#############################

print(df_to_ML_model.columns.tolist())

print(df_to_ML_model.shape)
df_to_ML_model_test1=df_to_ML_model.head(22308)
df_to_ML_model_test2=df_to_ML_model.iloc[22309:44615,:]
df_to_ML_model_test3=df_to_ML_model.tail(-1)

# Step 2: Connect the MongoDB
# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27017/")
# database (name of db)
db = client["real_state_database"]
# collection (name of table, I have only one table)
property1= db["Property1"]
# property2= db["Property2"]
# property3= db["Property3"]


# Step 4: Insert the Data into Database (some of db
# Step 4: Insert the Data into Database (some of db
# have to do convert the data frame into a dictionary(MongoDB uses JSON format data) and then
# insert it into the database.
# The other thing you should note that the Date column is set as Index of the Dataframe,
# therefore you have to reset the index before inserting.
df_to_ML_model_test1.reset_index(inplace=True)
data_dict1= df_to_ML_model_test1.to_dict("records")
property1.insert_one({"data":data_dict1})

#
# df_to_ML_model_test2.reset_index(inplace=True)
# data_dict2= df_to_ML_model_test2.to_dict("records")
# property2.insert_one({"data":data_dict2})
#
# df_to_ML_model_test3.reset_index(inplace=True)
# data_dict3= df_to_ML_model_test3.to_dict("records")
# property3.insert_one({"data":data_dict3})


# How to Load data from MongoDB to pandas dataframe?
data_from_db1 = property1.find_one()
df1 = pd.DataFrame(data_from_db1)
# df.set_index("_id",inplace=True)
#df.reset_index()
df1=df1["data"]
print(df1[0])