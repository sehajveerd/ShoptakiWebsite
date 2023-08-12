#!/usr/bin/python3
#!coding:utf-8
from bs4 import BeautifulSoup
import requests

import re
# U.S. Typical Home Value
# Change in Typical Home Value From Last Month
# U.S. Typical Monthly Rent
# Change in Typical Rent From Last Year
def main():
    url = 'https://www.zillow.com/research/'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,zh-CN;q=0.9",
        "Cache-Control": "no-cache",
        "Cookie": "JSESSIONID=DF9661D8FC09A8B515BA5FBD8CC459ED; zguid=24|%24511dc4af-33b6-4dff-b820-0e7426c62b19; zgsession=1|ce91228d-1424-4849-93f7-0b1e5b282fc6; zjs_user_id=null; zg_anonymous_id=%22d0662552-e16e-4626-a4e5-3ce41242c3ca%22; zjs_anonymous_id=%22511dc4af-33b6-4dff-b820-0e7426c62b19%22; AWSALB=SG6BonRC1PtdPEonHEr7WhNMMvY4A7Kv/NyfteYgEFh4DTeIeWbjFPli1ErqkK+EeZ86WJLEthwreY68ZaoCC/kCudypCZv5WC4exZQbI6KL+W8GG2ZopKBGWmHh; AWSALBCORS=SG6BonRC1PtdPEonHEr7WhNMMvY4A7Kv/NyfteYgEFh4DTeIeWbjFPli1ErqkK+EeZ86WJLEthwreY68ZaoCC/kCudypCZv5WC4exZQbI6KL+W8GG2ZopKBGWmHh",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'lxml')
    for ele in soup.select(".goldberg-wysiwyg p"):
        data = ele.get_text()
        print(data)

if __name__ == '__main__':
    main()
# Vacancy Rate in different state


import requests
from bs4 import BeautifulSoup

def main():
    url = "https://managecasa.com/articles/us-rental-occupancy-rates/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Cache-Control": "max-age=0",
        "Cookie": "qtrans_front_language=en;",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"99\", \"Chromium\";v=\"115\", \"Google Chrome\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response_object = requests.get(url, headers)
    html = response_object.text
    soup = BeautifulSoup(html, 'lxml')


    target_table = soup.select_one("body > article > section.t-article-grid > div > div.t-article-grid__main > div > table:nth-child(40)")


    for ele in target_table.select("td"):
        data = ele.get_text()
        print(data)

if __name__ == '__main__':
    main()

#	State	GDP	GDP per capita
def main():
    url = "https://wisevoter.com/state-rankings/gdp-by-state/"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,zh-CN;q=0.9",
        "Cache-Control": "no-cache",
        "Cookie": "_wpfuuid=bc137baa-2cb4-4bb8-a14b-37840443e0d7",
        "Pragma": "no-cache",
        "Sec-Ch-Ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response_object = requests.get(url, headers)
    html = response_object.text
    soup = BeautifulSoup(html, 'lxml')
    tr_object_list = soup.select('#shield-db-component-4 tr')

    for tr_obj in tr_object_list:
        text = ''
        for td_obj in tr_obj:
            td_text = td_obj.get_text()
            text = text + td_text + "\t"
        print(text)


if __name__ == '__main__':
    main()



