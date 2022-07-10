import requests
import pandas as pd
from slovnet import NER
from navec import Navec

#pip install openpyxl


#nlp = spacy.load('ru_core_news_md')
navec = Navec.load('../../navec_news_v1_1B_250K_300d_100q.tar')
ner = NER.load("../../slovnet_ner_news_v1.tar")
ner.navec(navec)

companies = ["Tripster", "Russia Discovery", "Sputnik 8", "Большая страна",
            "Travelata", "Знай места", "Utravelme", "We go trip"]
groups = ["https://vk.com/pvd_sochi", "https://vk.com/idem_pohod",
          "https://vk.com/pohodvgoru", "https://vk.com/altay", "https://vk.com/vtourisme",
          "https://vk.com/activealtay"]

token = "token"


def spans_set(spans, text):
    spans_list= []
    for span in spans:
        if span.type =='ORG':
            start_pos = span.start
            stop_pos = span.stop
            word = text[start_pos:stop_pos]
            spans_list.append(word)
    spans = set(spans_list)
    return spans


def company_similarity(company, text):
    company = company.lower()
    text = text.lower()

    intersection_set = list(set(company) & set(text))

    intersection_value = len(intersection_set) / len(text)
    return intersection_value


def vk_parser(list_compaies, urls):
    result = {company: [0, []] for company in list_compaies}
    start_from = None
    info = []
    offset = 0

    for url in urls:
        print(url)
        while True:
            """
            response = requests.get('https://api.vk.com/method/newsfeed.search', params={
                'access_token': token,
                'extend': 1,
                'q': [f'{company}'],
                'v': '5.131',
                'fields': ['name'],
            }).json()['response']["items"]
            """
            posts = requests.get("https://api.vk.com/method/wall.get", params={"domain": url.split("/")[-1],
                                                                               "count": 100,
                                                                               "access_token": token,
                                                                               "offset": str(offset),
                                                                               "v": "5.131"}).json()['response']['items']

            offset += 100

            if len(posts) == 0:
                break

            for post in posts:
                if post["text"]:
                    markup = ner(post["text"])
                    spans = markup.spans
                    spans = spans_set(spans, post["text"])

                    for company in companies:
                        count = 0
                        for span in spans:
                            if company_similarity(company, span) > 0.8:
                                count = count + 1

                                result[company][0] += 1
                                result[company][1].append((post["text"], url))

    return result


posts = vk_parser(companies, groups)

count = [(i, posts[i][0]) for i in posts]
message = pd.DataFrame([(i, j[1], j[0]) for i in posts for j in posts[i][1]])
message.to_excel("messages.xlsx", encoding="utf-8")

for i in groups:
    res = []
    for j in posts:
        messages = list(map(lambda x: x[0], filter(lambda x: x[1] == i, posts[j][1])))
        res.extend(list(zip([j]*len(messages), messages)))

    if len(res) > 0:
        res = pd.DataFrame(res)
        res.to_excel("{}.xlsx".format(i.split("/")[-1]), encoding="utf-8")