#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# get all houses in one area
import requests
import json

url = "https://zillow69.p.rapidapi.com/search"

querystring = {"location":"ca"}

headers = {
	"X-RapidAPI-Key": "e0976dab9amsh87b8bbf7c55ca91p16ecacjsnce1f4fe0c457",
	"X-RapidAPI-Host": "zillow69.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)
data = response.json()

beautiful_json = json.dumps(data, indent=4)

print(beautiful_json)


# In[ ]:


numberofHouses = len(data["props"])
address = data["props"][0]["address"]
street,city,end= address.strip().split(",")
state,zipcode = end.strip().split(" ")
#print(street,city,state,zipcode)
bedrooms = data["props"][0]["bedrooms"]
bathrooms = data["props"][0]["bathrooms"]
price = data["props"][0]["price"]
rent = data["props"][0]["rentZestimate"]
livingArea = data["props"][0]["livingArea"]
zpid = data["props"][0]["zpid"]


# In[ ]:


import pandas as pd

# data type
houses_data = {
    "zpid": [],
    "street": [],
    "city": [],
    "state": [],
    "zipcode": [],
    "bedrooms": [],
    "bathrooms": [],
    "price": [],
    "rent": [],
    "livingArea": []
}

# deal with every house
for house in data["props"]:
    address = house["address"]
    street, city, end = address.strip().split(",")
    state, zipcode = end.strip().split(" ")
    
    houses_data["zpid"].append(house["zpid"])
    houses_data["street"].append(street)
    houses_data["city"].append(city)
    houses_data["state"].append(state)
    houses_data["zipcode"].append(zipcode)
    houses_data["bedrooms"].append(house["bedrooms"])
    houses_data["bathrooms"].append(house["bathrooms"])
    houses_data["price"].append(house["price"])
    houses_data["rent"].append(house["rentZestimate"])
    houses_data["livingArea"].append(house["livingArea"])

# create pandas DataFrame
df = pd.DataFrame(houses_data)

# save
df.to_csv('houses_data.csv', index=False)


# In[ ]:


# start with this block
import pandas as pd
# read from csv
df = pd.read_csv('../datasets/Houses_data.csv')
df = df.dropna()

# calculate annual return
# this is an expected max return, not a net annual return
# Todo: add tax, insurance, maintenance, vacancy, property management fee
df["annualReturn"] = df["rent"] * 12 / df["price"]
df["annualReturn"] = df["annualReturn"]*100


# In[ ]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor

# encode string type data
le = LabelEncoder()
df['street'] = le.fit_transform(df['street'])
df['city'] = le.fit_transform(df['city'])
df['state'] = le.fit_transform(df['state'])
df['zipcode'] = le.fit_transform(df['zipcode'])

# split data into X and y
X = df.drop(columns=['annualReturn'])
y = df['annualReturn']

# split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# create model
model = RandomForestRegressor(n_estimators=15, random_state=42)

# train model
model.fit(X_train, y_train)

# predict on test
y_pred = model.predict(X_test)

# mae as metrics
mae = mean_absolute_error(y_test, y_pred)
print(f'The Mean Absolute Error of the model is: {mae}')


# In[ ]:




