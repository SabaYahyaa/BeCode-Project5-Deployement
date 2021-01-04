"""
This return the model that we create by Linear Regression,
It take the data set, and returns the model
param: cleaned_data is the cleaned csv file
"""

import joblib

import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.datasets import load_wine
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
from sklearn import ensemble


def model_func(df_cleaned):

    # #I can use immediately the following to get the cleaned df
    # f= Data_Cleaning_Exploration_Visualisation(df)

    # # extract only the features that will be used in LinearRegression
    X= df_cleaned.drop(['price'], axis=1).values
    y = df_cleaned['price'].values

    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=300, test_size=0.2)
    model = LinearRegression()

    #model = ensemble.GradientBoostingRegressor(n_estimators=400, max_depth=5, min_samples_split=7, learning_rate=0.1, loss='ls')
    #since, I will get test data from client, I will fit with all available data
    model.fit(X, y)

    #store the model in pickle file
    #joblib.dump(model, 'assets/model.sav')
    pickle.dump(model, open('asset/model.pkl', 'wb'))
    return ( )


if __name__=="__main__":
    # Reading the cleaned df
    from Cleaner_Train_Data import Cleaner_SalesData
    url = 'https://raw.githubusercontent.com/FrancescoMariottini/project3/main/inputs/all_sales_data.csv'
    ss = Cleaner_SalesData(url)
    df_cleaned = ss.cleaning_feature()
    model=model_func(df_cleaned)
    pickle.dump(model, open('asset/model.pkl', 'wb'))

