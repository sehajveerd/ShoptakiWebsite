import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


data = pd.read_csv("/Users/xiaohuidexiaojiaoqi/Desktop/Combined_house_data.csv", na_values=['Not Available'])


data.dropna(inplace=True)


selected_features = ['daysOnZillow', 'latitude', 'livingArea', 'lotAreaValue', 'price', 'priceForHDP', 'rentZestimate']
data = data[selected_features]


data["Net Operating Income"] = data["rentZestimate"]
data["Mortgage Payment"] = data["priceForHDP"]
data["Property Value"] = data["price"]
data["Loan Amount"] = data["priceForHDP"]

data["Annual Return"] = (data["Net Operating Income"] - data["Mortgage Payment"]) / data["Property Value"]
data["Capitalization Rate"] = (data["Net Operating Income"] / data["Property Value"]) * 100
data["Debt Yield"] = (data["Net Operating Income"] / data["Loan Amount"]) * 100

X = data.drop(columns=['Annual Return'])
y = data['Annual Return']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestRegressor(n_estimators=15, random_state=42)


model.fit(X_train, y_train)


y_pred = model.predict(X_test)


mae = mean_absolute_error(y_test, y_pred)
print(f'The Mean Absolute Error of the model is: {mae}')


data.to_csv("/Users/xiaohuidexiaojiaoqi/Desktop/Processed_house_data.csv", index=False)
