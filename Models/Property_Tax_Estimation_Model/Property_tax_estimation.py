#!/usr/bin/env python
# coding: utf-8

# Code for Modeling the Property Tax

# In[ ]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
import matplotlib.pyplot as plt
import pickle


# Creating the model and feature engineering :

# In[ ]:


df = pd.read_csv('Main_Table_of_RealEstate_with_tax.csv')
features = ['bedrooms', 'bathrooms', 'price', 'state','zestimate','priceForHDP','rentZestimate','zipcode']
target = 'taxAssessedValue'

X = df[features]
y = df[target]

le = LabelEncoder()
X['state'] = le.fit_transform(X['state'])

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

poly = PolynomialFeatures(degree=2, interaction_only=True, include_bias=False)
X_poly = poly.fit_transform(X_scaled)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Mean Squared Error:", mse)
print("R-squared Score:", r2)


# In[ ]:


df.corr()


# Plotting:

# In[ ]:


plt.scatter(y_test, y_pred)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'k--', lw=2)  # Identity line
plt.xlabel('Y_test')
plt.ylabel('Predicted')
plt.title('Prediction vs. Y_test')
plt.show()


# Creating the model and testing it against new data:

# In[ ]:


filename = 'linear_regression_model.sav'
pickle.dump(model, open(filename, 'wb'))

loaded_model = pickle.load(open('linear_regression_model.sav', 'rb'))

new_data = pd.read_csv('new_data.csv')

new_data['state'] = le.transform(new_data['state'])

new_predictions = loaded_model.predict(new_data[features])

new_data['PredictedTaxes'] = new_predictions

new_data.to_csv('new_data.csv', index=False)


# In[ ]:




