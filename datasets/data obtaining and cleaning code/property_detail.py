import json
import random

import requests
import pandas as pd
import csv
import time


def fetch_data(loc):
    url = "https://zillow56.p.rapidapi.com/property"
    querystring = {"zpid": loc}

    # headers = {
    #     "X-RapidAPI-Key": "0c737feaecmsh8f5d2858c8960adp1d4ca1jsnc7db9cb645d9",
    #     "X-RapidAPI-Host": 'zillow56.p.rapidapi.com'
    # }
    headers = {
        'X-RapidAPI-Key': 'e0976dab9amsh87b8bbf7c55ca91p16ecacjsnce1f4fe0c457',
        'X-RapidAPI-Host': 'zillow56.p.rapidapi.com'
    }
    random_sleep_time = random.randint(1, 3)
    res = requests.get(url, headers=headers, params=querystring)
    time.sleep(random_sleep_time)  # wait for response
    print(res.text)
    temp = json.loads(res.text)
    return temp


def process_data():
    txt_file_path = 'used.txt'
    data_set = set()
    with open(txt_file_path, 'r') as txt_file:
        for line in txt_file:
            value = line.strip()  # 去除行尾的换行符
            data_set.add(value)
    # 创建一个空的set来存储数据
    df = pd.read_csv('Latest_maintable.csv')
    count = 0
    all_responses = []
    new_data = []
    for zpId in list(df["zpid"]):
        zp_id = str(zpId)
        print(zp_id)
        if zp_id not in data_set:
            data = fetch_data(zp_id)
            all_responses.append(data)
            new_data.append(zp_id)
            count = count + 1
            if count == 10 & len(data_set) == 0:
                df = pd.DataFrame(all_responses)
                df.fillna("null", inplace=True)
                df.to_csv("property_details.csv", index=False)
                all_responses = []
            if count == 10 & len(data_set) > 0:
                df_1 = pd.DataFrame(all_responses)
                df_1.fillna("null", inplace=True)
                with open("property_details.csv", 'a', newline='') as file:
                    df_1.to_csv(file, index=False, header=False)
                all_responses = []
                with open(txt_file_path, 'a') as txt_file:
                    for value in new_data:
                        txt_file.write(str(value) + '\n')
                new_data = []
            if count % 10 == 0 & count != 10:
                df_1 = pd.DataFrame(all_responses)
                df_1.fillna("null", inplace=True)
                with open("property_details.csv", 'a', newline='') as file:
                    df_1.to_csv(file, index=False, header=False)
                all_responses = []
                with open(txt_file_path, 'a') as txt_file:
                    for value in new_data:
                        txt_file.write(str(value) + '\n')
                new_data = []

    df_1 = pd.DataFrame(all_responses)
    df_1.fillna("null", inplace=True)
    with open("property_details.csv", 'a', newline='') as file:
        df_1.to_csv(file, index=False, header=False)


if __name__ == "__main__":
    process_data()
