import requests
import time
import json

API_URL = "https://zillow56.p.rapidapi.com/search"
API_KEY = "c9cdae6251msh7bc8cc39d8e31efp159734jsn5394d2d48546"
API_HOST = "zillow56.p.rapidapi.com"


def fetch_data(querystring):
    headers = {"X-RapidAPI-Key": API_KEY, "X-RapidAPI-Host": API_HOST}

    response = requests.get(API_URL, headers=headers, params=querystring)
    time.sleep(1) # wait for response
    return response.json()


def output_json(data):
    properties = data['results']
    field_names = list(properties[0].keys())

    filename = "./datasets/sample_output.json"
    with open(filename, 'w', newline='') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    querystring = {"location": "los angeles, ca", "page": "1"}
    response = fetch_data(querystring)
    output_json(response)
