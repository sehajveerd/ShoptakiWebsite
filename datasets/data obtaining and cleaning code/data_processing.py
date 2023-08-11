import pandas as pd

df_1 = pd.read_csv('property_details_updated_test.csv')
df = pd.read_csv('Latest_maintable.csv')

unit_data = df[['zpid', 'unit']]
merge_df = pd.merge(df_1, unit_data, on='zpid', how='left')

merge_df.to_csv('merge_data.csv', index=False)

# streets = []
# citys = []
# zipcodes = []
# states = []
# homeStatuses = []
# homeTypes = []
# bedrooms = []
# bathrooms = []
# latitudes = []
# longitudes = []
# imageUrls = []
# units = []
# prices = []
# livingAreas= []
# zestimates = []
# rentZestimates = []
# zpids = []
# daysOnZillows= []

# csv_data = {"street": streets, "city": citys, "zipcode": zipcodes, "state": states, "homeStatus": homeStatuses,
#             "homeType": homeTypes, "bedrooms": bedrooms, "bathrooms": bathrooms, "latitude": latitudes, "longitude": longitudes,
#             "imageUrl": imageUrls, "unit": units, "price": prices, "livingArea": livingAreas,  "zestimate": zestimates,
#             "rentZestimate": rentZestimates, "zpid": zpids, "daysOnZillow": daysOnZillows}

# for street, city, zipcode, state, homeStatus, homeType, bedrooms, bathrooms, latitude, longitude, imageUrl, unit, price,livingArea, zestimate, rentZestimate, zpid, daysOnZillow in zip(list(df['streetAddress']), list(df['city']), list(df['zipcode']), list(df['state']), list(df['homeStatus']),list(df['homeType']), list(df['bedrooms']),list(df['bathrooms']), list(df['latitude']), list(df['longitude']), list(df['photos']), list(df['unit']), list(df['price']), list(df['livingArea']), list(df['zestimate']), list(df['rentZestimate']), list(df['zpid']), list(df['daysOnzillow'])):
