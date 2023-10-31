from fredapi import Fred
import ssl
import pandas as pd

# Ignore certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

# Replace with your FRED API key
api_key = 'dde6bdd862d1bb841d4e59726c28d52a'
fred = Fred(api_key=api_key)

# Get GDP data
gdp_data = fred.get_series('GDP')

# Get interest rate data, e.g., Federal Funds Rate
interest_rate_data = fred.get_series('FEDFUNDS')

# Store the data in a DataFrame
data = pd.DataFrame({'GDP': gdp_data, 'Interest Rate': interest_rate_data})

# Print all the data
print("All Data:")
print(data)

# Save the data to a CSV file
data.to_csv('macroeconomic_data.csv', index=False)

