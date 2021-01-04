import pandas as pd
import numpy as np
import json
import re

""" 
Peprocess our data, to match the client data,
I will clean our data, such that the cleaned features will be as below:
{
    "data": {
            "area": int,
            "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
            "rooms-number": int,
            "zip-code": int,
            "land-area": Optional[int],
            "garden": Optional[bool],
            "garden-area": Optional[int],
            "equipped-kitchen": Optional[bool],
            "full-address": Optional[str],
            "swimmingpool": Opional[bool],
            "furnished": Opional[bool],
            "open-fire": Optional[bool],
            "terrace": Optional[bool],
            "terrace-area": Optional[int],
            "facades-number": Optional[int],
            "building-state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
    }
}
"""

class Cleaner_SalesData:
    """ Utility class that cleans real estate sale offers data from a CSV file into a pandas DataFrame for further work on it"""
    def __init__(self, url):
        self.url = url
        self.sales_data = None
        self.cleaned = False

    def cleaning_feature(self):

        #if we have csv files
        na_identifiers = ['NA', 'None', 'Not specified', 'NaN', 'NAN']
        self.sales_data = pd.read_csv(self.url, sep=",", skipinitialspace=True, na_values=na_identifiers, low_memory=False)
        # drop these features ['source', 'hyperlink', 'sale', 'land_plot_surface']
        self.sales_data.drop('hyperlink', axis='columns', inplace=True)
        self.sales_data.drop('source', axis='columns', inplace=True)
        self.sales_data.drop('sale', axis='columns', inplace=True)
        self.sales_data.drop('land_plot_surface', axis='columns', inplace=True)

        self.sales_data.rename(columns={'building_state': 'building-state','garden_area': 'garden-area','property_subtype': 'property-type','postcode': 'zip-code','facades_number': 'facades-number','rooms_number': 'rooms-number','terrace_area': 'terrace-area','land_surface': 'land-area','open_fire': 'open-fire','kitchen_has': 'equipped-kitchen', 'swimming_pool_has':'swimmingpool'}, inplace=True)
        # #self.sales_data.drop('building-state', axis='columns', inplace=True)
        #33333333333333333333333333333333333333333333333333333


        ###################################
        ###################################
        #######    Boolean Features, cleaning
        ###################################
        ###################################
        #Optional, equipped-kitchen
        self.sales_data['equipped-kitchen']=self.sales_data['equipped-kitchen'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
        #If I have missing value, I replace it with the highest frequency value
        self.sales_data['equipped-kitchen']=self.sales_data['equipped-kitchen'].fillna(self.sales_data['equipped-kitchen'].mode().iloc[0])
        #cast to boolean
        self.sales_data['equipped-kitchen'] = self.sales_data['equipped-kitchen'].apply(lambda x: bool(x))

        # Optional, furnished
        self.sales_data['furnished']=self.sales_data['furnished'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
        self.sales_data['furnished']=self.sales_data['furnished'].fillna(self.sales_data['furnished'].mode().iloc[0])


        #  swimmingpool
        self.sales_data['swimmingpool']=self.sales_data['swimmingpool'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
        self.sales_data['swimmingpool']=self.sales_data['swimmingpool'].fillna(self.sales_data['swimmingpool'].mode().iloc[0])
        self.sales_data['swimmingpool'] = self.sales_data['swimmingpool'].apply(lambda x: bool(x))

        #Optional, open-fire
        self.sales_data['open-fire']=self.sales_data['open-fire'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
        self.sales_data['open-fire']=self.sales_data['open-fire'].fillna(self.sales_data['open-fire'].mode().iloc[0])
        self.sales_data['open-fire'] = self.sales_data['open-fire'].apply(lambda x: bool(x))

        # terrace
        self.sales_data['terrace']=self.sales_data['terrace'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
        self.sales_data['terrace']=self.sales_data['terrace'].fillna(self.sales_data['terrace'].mode().iloc[0])
        self.sales_data['terrace'] = self.sales_data['terrace'].apply(lambda x: bool(x))

        #Optional, garden
        self.sales_data['garden']=self.sales_data['garden'].apply(lambda x: Cleaner_SalesData.bool_or_keep(x))
        self.sales_data['garden']=self.sales_data['garden'].fillna(self.sales_data['garden'].mode().iloc[0])
        self.sales_data['garden'] = self.sales_data['garden'].apply(lambda x: bool(x))

        # ###################################
        # ###################################
        # #######    Area Features
        # ###################################
        # ###################################
        # #area, remove m2
        self.sales_data['area'] = self.manage_AreaFeature(self.sales_data['area'])

        # #land-area": Optional[int],
        self.sales_data['land-area']=self.manage_AreaFeature(self.sales_data['land-area'])

        #"terrace-area": Optional[int],
        self.sales_data['terrace-area']=self.manage_AreaFeature(self.sales_data['terrace-area'])

        #garden-area": Optional[int],
        self.sales_data['garden-area']=self.manage_AreaFeature(self.sales_data['garden-area'])

        # ###################################
        # ###################################
        # #######    Number Features
        # ###################################
        # ###################################
        # #"rooms-number": int,
        # #remove outliers
        to_be_deleted_filter = self.sales_data['rooms-number'].apply(lambda x: x == 0 or x >= 100)
        self.sales_data.loc[to_be_deleted_filter, 'rooms-number'] = None
        self.sales_data['rooms-number'] = self.sales_data['rooms-number'].fillna(self.sales_data['rooms-number'].mode().iloc[0])
        self.sales_data['rooms-number'] = self.sales_data['rooms-number'].apply(lambda x: int(x))

        #facades-number": Optional[int],
        to_be_deleted_filter = self.sales_data['facades-number'].apply(lambda x: x == 0 or x > 4)
        self.sales_data.loc[to_be_deleted_filter, 'facades-number'] = None
        self.sales_data['facades-number'] = self.sales_data['facades-number'].fillna(self.sales_data['facades-number'].mode().iloc[0])
        self.sales_data['facades-number'] = self.sales_data['facades-number'].apply(lambda x: int(x))

        # ###################
        # ######### TO DO, need TO CHECK AGAIN
        # #################
        #"zip-code": int, we could have nan input
        self.sales_data['zip-code'] = self.sales_data['zip-code'].fillna(0)
        self.sales_data['zip-code'] = self.sales_data['zip-code'].apply(lambda x: int(x))
        self.sales_data= self.sales_data[self.sales_data['zip-code'] != 0]

        # # #"property-type": "APARTMENT" | "HOUSE" | "OTHERS",
        self.sales_data['property-type']=self.sales_data['property-type'].apply(lambda x: Cleaner_SalesData.property_or_keep(x))
        self.sales_data['property-type']= self.sales_data['property-type'].fillna(self.sales_data['property-type'].mode().iloc[0])
        # ######## generate dummies
        # create dummies, the prefix "", store it in another varialbe
        dummies_region = pd.get_dummies(self.sales_data['property-type'], prefix="property-type")
        # concatenate, dummies with the original df
        self.sales_data = pd.concat([self.sales_data, dummies_region], axis=1, sort=False)
        # drop the region
        self.sales_data.drop('property-type', axis="columns", inplace=True)

        # #building-state"
        self.sales_data['building-state'] = self.sales_data['building-state'].apply(lambda x: Cleaner_SalesData.categorize_state(x))
        highest_categorized = self.sales_data['building-state'].value_counts().index[0]
        self.sales_data['building-state'] = self.sales_data['building-state'].fillna(highest_categorized)

        #     #### if buildin-state is exist, the generate dummies
        # get the dummies of categorize_state:::: Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
        dummies_region = pd.get_dummies(self.sales_data['building-state'] , prefix="building-state")
        self.sales_data= pd.concat([self.sales_data, dummies_region], axis=1, sort=False)
        self.sales_data.drop('building-state', axis="columns", inplace=True)  # drop_first="True" if we need to drop the first one

        #since we do not have TO REBUILD, I will added
        self.sales_data['building-state_TO REBUILD']=np.zeros(self.sales_data.shape[0])


        self.sales_data=self.sales_data[['area','rooms-number','zip-code', 'land-area','garden','garden-area',
'equipped-kitchen','swimmingpool','furnished','open-fire','terrace','terrace-area','facades-number',
'property-type_APARTMENT','property-type_HOUSE','property-type_OTHERS','building-state_NEW','building-state_GOOD',
'building-state_TO RENOVATE','building-state_JUST RENOVATED','building-state_TO REBUILD','price']]

        #price cleaning
        self.sales_data['price']=self.sales_data['price'].apply( lambda x: Cleaner_SalesData.price_converter(x))

        #remove duplicated
        self.sales_data.drop_duplicates(subset=['zip-code','property-type_APARTMENT','property-type_HOUSE','property-type_OTHERS', 'price', 'area'], inplace=True)
        self.sales_data.dropna( inplace=True)
        return (self.sales_data)
        #return (self.sales_data['price'].isnull().sum())

    @staticmethod
    def price_converter(x):
        x=str(x)
        # removing non-digit heading and trailiong characters
        x = re.sub(r'\D+$', '', re.sub(r'^\D+', '', x))
        # removing trailing non-digit and dot characters until the last '€' character
        x = re.sub(r'€(.|\D)*$', '', x)
        x = x.replace(',', '')
        # we expect only digits or a dot after replacing commas with an empty string, so we should be able to convert if
        # if not possible we catch the exceptionproperty_subtype
        try:
            return float(x)
        except ValueError:
            return None

    @staticmethod
    def categorize_state(value):
        to_renovate = ['TO_RENOVATE', 'TO_BE_DONE_UP', 'TO_RESTORE', 'old', 'To renovate', 'To be done up',
                       'To restore', "TO RENOVATE"]
        good = ['GOOD', 'Good']
        renovated = ['JUST_RENOVATED', 'Just renovated', "JUST RENOVATED"]
        new = ['New',"NEW", 'AS_NEW', 'As new']
        to_rebuild=["TO REBUILD","TO_REBUILD", "To rebuild"]
        category = None  # default category (corresponds to values = '0')
        if value in to_renovate:
            category = "TO RENOVATE"
        elif value in good:
            category = "GOOD"
        elif value in renovated:
            category = "JUST RENOVATED"
        elif value in new:
            category = "NEW"
        elif value in to_rebuild:
            category = "TO REBUILD"
        return category


    def manage_AreaFeature(self, Ser):
        #remove m2
        Ser= Ser.apply(lambda x: Cleaner_SalesData.area_remove_m2(x))
        #fill in the empty cells
        #Ser.fillna(Ser.median(), inplace=True)
        Ser= Ser.fillna(Ser.median())
        #cast to int
        Ser = Ser.apply(lambda x: int(x))
        return (Ser)

    @staticmethod
    def property_or_keep(x):
        try:
            if x in ["APARTMENT", "Apartment"]:
                return ("APARTMENT")
            elif x in ["HOUSE", "House"]:
                return ("HOUSE")
            elif str(x).isdigit():
                return None
            elif x not in ["APARTMENT", "Apartment","HOUSE", "House"]:
                return ("OTHERS")
        except ValueError:
                 return None

    @staticmethod
    def bool_or_keep(x):
        try:
            if x in [1, "1", "TRUE", "true", "True",True,"YES", "yes", "Yes"]:
                return (True)
            elif x in [0, "0", "FALSE", "false", "False",False,"NO", "no", "No"]:
                return (False)
        except ValueError:
            return (None)

    @staticmethod
    # a single integer number is extracted from area to remove the m2 measurement units.
    # this simple method was adopted since no commas were found in area field.
    def area_remove_m2(x):
        try:
            return int(x)
        except ValueError:
            x=str(x)
            numbers = [int(s) for s in x.split() if s.isdigit()]
            if len(numbers) == 1:
                return float(numbers[0])
            elif len(numbers) > 1:
                return False
            else:
                return None


if __name__=="__main__":
    url = 'https://raw.githubusercontent.com/FrancescoMariottini/project3/main/inputs/all_sales_data.csv'
    ss=Cleaner_SalesData(url)
    df_cleaned=ss.cleaning_feature()
    print(df_cleaned)
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split

    X = df_cleaned.drop(['price'], axis=1).values

    y = df_cleaned['price'].values
    #
    # # X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=300, test_size=0.2)
    model = LinearRegression()
    # # since, I will get test data from client, I will fit with all available data
    model.fit(X, y)
    import pickle

    pickle.dump(model, open('model.pkl', 'wb'))
    # print(df_cleaned.shape)


