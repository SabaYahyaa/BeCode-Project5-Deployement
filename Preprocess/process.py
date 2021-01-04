"""
this generates a preprocesed data and preprocessed json file
testing_features=Processed_JSON(url_json)
this is to run the code
url_json is the input file,
you will get preprocessed_data.json on the folder: preprocess and the X_test (testing_features)
"""
import pandas as pd
from Preprocess.Clean import Cleaner_SalesData
import json


def Processed_JSON(url_json):
    #from Clean import Cleaner_SalesData
    import json
    preprocessed_dict=Cleaner_SalesData(url_json)
    r=preprocessed_dict.cleaning_feature()

    # #we do not need to store the cleaned json file, only process it an get the prediction
    # # #write the json, this is not necessary
    # with open("preprocessed_data.json", "w") as p1:
    #     json.dump(r, p1)
    #
    # # # If we want to load the preprocessed data that is stored in JSON
    # data_processed = json.load(open('preprocessed_data.json'))
    # print(data_processed )
    # z={'0': {'area': 300, 'rooms-number': 2, 'zip-code': 1050, 'land-area': 200, 'garden': True, 'garden-area': 100, 'equipped-kitchen': True, 'swimmingpool': False, 'furnished': True, 'open-fire': True, 'terrace': False, 'terrace-area': 0, 'facades-number': 2, 'property-type_APARTMENT': 1, 'property-type_2': 0.0, 'property-type_3': 0.0, 'building-state_NEW': 1, 'building-state_2': 0.0, 'building-state_3': 0.0, 'building-state_4': 0.0, 'building-state_5': 0.0}}

    features=r[0]
    testing_features=[]
    testing_features.append(features['area'])
    testing_features.append(features['rooms-number'])
    testing_features.append(features['zip-code'])
    testing_features.append(features['land-area'])
    testing_features.append(features['garden'])
    testing_features.append(features['garden-area'])
    testing_features.append(features['equipped-kitchen'])
    testing_features.append(features['swimmingpool'])
    testing_features.append(features['furnished'])
    testing_features.append(features['open-fire'])
    testing_features.append(features['terrace'])
    testing_features.append(features['terrace-area'])
    testing_features.append(features['facades-number'])

    if 'property-type_APARTMENT' in features:
        testing_features.append(features['property-type_APARTMENT'])
        testing_features.append(features['property-type_2'])
        testing_features.append(features['property-type_3'])
    elif 'property-type_HOUSE' in features:
        testing_features.append(features['property-type_2'])
        testing_features.append(features['property-type_HOUSE'])
        testing_features.append(features['property-type_3'])
    elif 'property-type_OTHERS' in features:
        testing_features.append(features['property-type_2'])
        testing_features.append(features['property-type_3'])
        testing_features.append(features['property-type_OTHERS'])
    else:
        testing_features.append(0)
        testing_features.append(0)
        testing_features.append(0)

    if 'building-state_NEW' in features:
        testing_features.append(features['building-state_NEW'])
        testing_features.append(features['building-state_2'])
        testing_features.append(features['building-state_3'])
        testing_features.append(features['building-state_4'])
        testing_features.append(features['building-state_5'])
    elif 'building-state_GOOD' in features:
        testing_features.append(features['building-state_2'])
        testing_features.append(features['building-state_GOOD'])
        testing_features.append(features['building-state_3'])
        testing_features.append(features['building-state_4'])
        testing_features.append(features['building-state_5'])

    elif 'building-state_TO RENOVATE' in features:
        testing_features.append(features['building-state_2'])
        testing_features.append(features['building-state_3'])
        testing_features.append(features['building-state_TO RENOVATE'])
        testing_features.append(features['building-state_4'])
        testing_features.append(features['building-state_5'])

    elif 'building-state_JUST RENOVATED' in features:
        testing_features.append(features['building-state_2'])
        testing_features.append(features['building-state_3'])
        testing_features.append(features['building-state_4'])
        testing_features.append(features['building-state_JUST RENOVATED'])
        testing_features.append(features['building-state_5'])

    elif 'building-state_TO REBUILD' in features:
        testing_features.append(features['building-state_2'])
        testing_features.append(features['building-state_3'])
        testing_features.append(features['building-state_4'])
        testing_features.append(features['building-state_5'])
        testing_features.append(features['building-state_TO REBUILD'])

    else:
        testing_features.append(0)
        testing_features.append(0)
        testing_features.append(0)
        testing_features.append(0)
        testing_features.append(0)

    return(testing_features) #this should go to the prediction folder

if __name__=="__main__":
    #you can specify
    url_json = 'Project5-Api_deployment/asset/input_data.json'
    url_json = 'input_data.json'

    # get the testing list, you need to add extra dimension to it
    testing_features=Processed_JSON(url_json)
    # print(testing_features)


    #
    # # If we want to load the preprocessed data that is stored in JSON
    # data_processed = json.load(open('preprocessed_data.json'))
    # print(data_processed )
    # z={'0': {'area': 300, 'rooms-number': 2, 'zip-code': 1050, 'land-area': 200, 'garden': True, 'garden-area': 100, 'equipped-kitchen': True, 'swimmingpool': False, 'furnished': True, 'open-fire': True, 'terrace': False, 'terrace-area': 0, 'facades-number': 2, 'property-type_APARTMENT': 1, 'property-type_2': 0.0, 'property-type_3': 0.0, 'building-state_NEW': 1, 'building-state_2': 0.0, 'building-state_3': 0.0, 'building-state_4': 0.0, 'building-state_5': 0.0}}




##############################################
#############################################
########     Emre preprocess
##############################################
##############################################
# def preprocess(new_json_name):
#    # url_json='Datasets/'+str(new_json_name)
#     url_json = 'input_data.json'
#     ss=Cleaner_SalesData(url_json)
#     new_json_df = ss.cleaning_feature()
#     print(new_json_df)
#     cleaned_json_df = pd.DataFrame()
#     cleaned_json_df['zip-code'] = new_json_df['zip-code']
#     cleaned_json_df['area'] = new_json_df['area']
#     cleaned_json_df['rooms_number'] = new_json_df['rooms-number']
#     cleaned_json_df['garden'] = new_json_df['garden']
#     cleaned_json_df['garden_area'] = new_json_df['garden-area']
#     cleaned_json_df['terrace'] = new_json_df['terrace']
#     cleaned_json_df['terrace_area'] = new_json_df['terrace-area']
#     cleaned_json_df['land_surface'] = new_json_df['land-area']
#     cleaned_json_df['open_fire'] = new_json_df['open-fire']
#     cleaned_json_df['swimming_pool_has'] = new_json_df['swimmingpool']
#     cleaned_json_df['equipped_kitchen_has'] = new_json_df['equipped-kitchen']
#     cleaned_json_df['furnished'] = new_json_df['furnished']
#     cleaned_json_df['property_subtype'] = new_json_df['property-type']
#     cleaned_json_df['building_state'] = new_json_df['building-state']
#
#     cleaned_json_df[['APARTMENT', 'HOUSE', 'OTHERS', 'GOOD',
#            'JUST RENOVATED', 'NEW', 'TO REBUILD', 'TO RENOVATE']] = 0
#
#     for i in range(len(cleaned_json_df)):
#         property_name = cleaned_json_df.loc[i, 'property_subtype']
#         building_state_name = cleaned_json_df.loc[i, 'building_state']
#         cleaned_json_df.loc[i, property_name] = 1
#         cleaned_json_df.loc[i, building_state_name] = 1
#
#     cleaned_json_df.drop(['property_subtype', 'building_state'], axis=1, inplace=True)
#     cleaned_json_df = cleaned_json_df.astype('float64')
#
#     return cleaned_json_df




#
#
# if __name__=="__main__":
#     #url = 'https://raw.githubusercontent.com/FrancescoMariottini/project3/main/inputs/all_sales_data.csv'
#     url_json='input_data.json'
#     cleaned_json_df=preprocess(url_json)
#     #print(cleaned_json_df)

