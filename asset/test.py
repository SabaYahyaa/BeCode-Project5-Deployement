import pickle
import numpy as np
import json

modele=pickle.load(open('model.pkl','rb'))

data_processed = json.load(open('Project5-Api_deployment/asset/input_data.json'))
print(data_processed)

features=data_processed["0"]
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

print(testing_features)

y_pred_new = (modele.predict([testing_features]))
print(y_pred_new)