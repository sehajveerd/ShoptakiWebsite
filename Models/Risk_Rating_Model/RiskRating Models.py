import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor

input_file = '/Users/mac/Desktop/Latest_maintable.csv'
output_file = '/Users/mac/Desktop/Latest_maintable_risk_rating_score.csv'

df = pd.read_csv(input_file)


home_type_mapping = {
    'LOT': 1,
    'SINGLE_FAMILY': 2,
    'CONDO': 3,
    'MANUFACTURED': 4
}
df['homeType_num'] = df['homeType'].map(home_type_mapping)


price_coeff = 0.002
priceForHDP_coeff = 0.0006
daysOnZillow_coeff = 0.0005
livingArea_coeff = 0.0012
lotAreaValue_coeff = 0.0005
homeType_coeff = 0.0002
rentZestimate_coeff = -0.0003


df['investment_risk'] = (
    df['price'] * price_coeff +
    df['priceForHDP'] * priceForHDP_coeff +
    df['daysOnZillow'] * daysOnZillow_coeff +
    df['livingArea'] * livingArea_coeff +
    df['lotAreaValue'] * lotAreaValue_coeff +
    df['homeType_num'] * homeType_coeff +
    df['rentZestimate'].fillna(0) * rentZestimate_coeff  # Fill missing 'rentZestimate' values with 0 for calculation
)


selected_features = ['daysOnZillow', 'latitude', 'livingArea', 'lotAreaValue', 'price', 'priceForHDP', 'rentZestimate']


df.dropna(subset=['rentZestimate'], inplace=True)

df.dropna(subset=selected_features + ['investment_risk'], inplace=True)


X = df[selected_features]
y = df['investment_risk']


imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

scaler = MinMaxScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


linear_model = LinearRegression()
gbt_model = GradientBoostingRegressor(random_state=42)
rf_model = RandomForestRegressor(random_state=42)

linear_model.fit(X_train, y_train)
gbt_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)


y_pred_linear = linear_model.predict(X_test)
y_pred_gbt = gbt_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)


df['Predicted Score (Linear)'] = linear_model.predict(X)
df['Predicted Score (GBT)'] = gbt_model.predict(X)
df['Predicted Score (RF)'] = rf_model.predict(X)

df['Average Score'] = df[['Predicted Score (Linear)', 'Predicted Score (GBT)', 'Predicted Score (RF)']].mean(axis=1)

scaler = MinMaxScaler(feature_range=(0, 100))
df['Predicted Score (Linear)'] = scaler.fit_transform(df['Predicted Score (Linear)'].values.reshape(-1, 1))
df['Predicted Score (GBT)'] = scaler.fit_transform(df['Predicted Score (GBT)'].values.reshape(-1, 1))
df['Predicted Score (RF)'] = scaler.fit_transform(df['Predicted Score (RF)'].values.reshape(-1, 1))
df['Average Score'] = scaler.fit_transform(df['Average Score'].values.reshape(-1, 1))

df['Linear Risk Level'] = pd.cut(df['Predicted Score (Linear)'], bins=[0, 33.3, 66.6, 100], labels=['Low', 'Medium', 'High'])
df['GBT Risk Level'] = pd.cut(df['Predicted Score (GBT)'], bins=[0, 33.3, 66.6, 100], labels=['Low', 'Medium', 'High'])
df['RF Risk Level'] = pd.cut(df['Predicted Score (RF)'], bins=[0, 33.3, 66.6, 100], labels=['Low', 'Medium', 'High'])

df['Average Risk Level'] = pd.cut(df['Average Score'], bins=[0, 33.3, 66.6, 100], labels=['Low', 'Medium', 'High'])

df = df[['zpid', 'price','priceForHDP','daysOnZillow', 'price', 'livingArea','lotAreaValue','homeType', 'rentZestimate',
         'Predicted Score (Linear)', 'Linear Risk Level', 'Predicted Score (GBT)', 'GBT Risk Level',
         'Predicted Score (RF)', 'RF Risk Level', 'Average Score', 'Average Risk Level', 'investment_risk']]


df.to_csv(output_file, index=False)

print("Generated CSV file with predicted risk scores and risk levels:", output_file)
