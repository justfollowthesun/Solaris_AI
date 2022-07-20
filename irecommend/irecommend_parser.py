import json
from bs4 import BeautifulSoup
import requests

def review_parser(url):

    """
    The function of parsing data from the product reviews page. 
    Input: url to the product page (ex. "https://irecommend.ru/content/besprovodnye-naushniki-sportbeats-bluetooth"). 
    Return: A json file with recorded product average rating, usernames, review texts, and user ratings.
    """

    page = requests.get(url)
    html = page.text
    soup = BeautifulSoup(html, "lxml")
    reviews = soup.find_all("li", class_ = "item")

    review_data = {}

    product_name = soup.find("span", class_="fn").text
    product_rating = float(soup.find("span", class_="rating").text)
    num_votes = soup.find("span", class_="total-votes").text

    review_data = {
        'product_name': product_name,
        'product_rating': product_rating,
        'num_votes': num_votes,
    }

    for id, review_i in enumerate(reviews):
        reviewer_name = review_i.find("div", class_="authorName").text
        review_text = review_i.find("span", class_="reviewTeaserText").text
        review_rating = review_i.find("div", class_="fivestarWidgetStatic fivestarWidgetStatic-vote fivestarWidgetStatic-5")
        review_rating = len(review_rating.find_all("div", class_="on"))

        reviews = {
            'reviewer_name': reviewer_name, 
            'review_text': review_text, 
            'review_rating': review_rating
            }

        review_data[f'{id}'] = reviews

    with open (f'{product_name}.json', 'w', encoding="utf-8") as f:
        json.dump(review_data, f)

# check:

# review_parser("https://irecommend.ru/content/besprovodnye-naushniki-sportbeats-bluetooth")
# with open ('Беспроводные наушники SportBeats Bluetooth.json', 'r', encoding="utf-8") as f:
    # reviews = json.load(f)