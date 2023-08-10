import pandas as pd
import requests


def get_geocode(address, api_key):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    print(data)
    if data['status'] == 'OK':
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        print(longitude)
        print(longitude)
        print("OK")
        return latitude, longitude
    else:
        return None, None


# Your Google Maps API key
api_key = "AIzaSyDclHcSFoO7vBM8JjzWJ0lmkWET4NyVgT0"

# Replace 'cvs_data.csv' with the path to your CSV file
csv_file_path = 'property_details_updated_test.csv'
df = pd.read_csv(csv_file_path)

for index, row in df.iterrows():
    abbreviatedAddress = row['abbreviatedAddress']
    cityAddress = row['city']
    if isinstance(abbreviatedAddress, str) & isinstance(cityAddress, str):
        address = abbreviatedAddress + ',' + cityAddress
        address = str(address)
        latitude = row['latitude']
        longitude = row['longitude']
        # print(latitude)
        if pd.isnull(latitude) or pd.isnull(longitude):  # Check for missing values
            # print("OK")
            new_latitude, new_longitude = get_geocode(address, api_key)
            df.at[index, 'latitude'] = new_latitude if pd.notnull(new_latitude) else latitude
            df.at[index, 'longitude'] = new_longitude if pd.notnull(new_longitude) else longitude

# Save the updated DataFrame to the same CSV file
df.to_csv(csv_file_path, index=False)
