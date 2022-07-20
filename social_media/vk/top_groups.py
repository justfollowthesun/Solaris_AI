import requests
import pandas as pd
import time
from slovnet import NER
from navec import Navec

#pip install openpyxl

companies = [("Tripster", "https://experience.tripster.ru/"), ("Russia Discovery", "https://www.russiadiscovery.ru/"),
             ("Sputnik 8", "https://www.sputnik8.com/"), ("Большая страна", "https://bolshayastrana.com/"),
             ("Travelata", "https://travelata.ru/"), ("Знай места", "https://znaimesta.ru/"),
             ("Utravelme", "http://utravelme.com/"), ("We go trip", "https://wegotrip.com/")]


token = "token"


def times(days:int) -> int:
    end_time = (int(time.time()))
    start_time = end_time - days*86400
    return start_time


def groups_companies(companies, days):
    result = dict()
    start_time = times(days)

    for company in companies:
        next_from = None
        while True:
            print(company, next_from)

            par = {
                    'access_token': token,
                    'extended': 1,
                    'q': [f'{company[0]}', f'{company[1]}'],
                    'start_time': start_time,
                    'v': '5.131'
                }

            if next_from is not None:
                par['start_from'] = next_from

            try:
                response = requests.get('https://api.vk.com/method/newsfeed.search', params=par).json()['response']
            except:
                pass

            if response:
                groups = {i["id"]: i["name"] for i in response['groups']}
                for post in response["items"]:
                    if post['owner_id'] < 0:
                        result[groups[(-post['owner_id'])]] = 1 if groups[(-post['owner_id'])] not in result.keys() else result[groups[-post['owner_id']]] + 1

            if 'next_from' in response.keys():
                next_from = response['next_from']
            else:
                break

    return result


result = groups_companies(companies, 30)

import pandas

result = pd.DataFrame([(i, result[i]) for i in result.keys()])
print(result)
result = result.sort_values(by=1, ascending=False)
result.to_excel("result.xlsx", encoding="utf-8")