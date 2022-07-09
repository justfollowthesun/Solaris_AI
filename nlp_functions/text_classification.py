from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
from yandex_translate import YandexTranslate
from nlp_keys import YANDEX_TOKEN
from langdetect import detect
import requests
import spacy


def translate(text, IAM_TOKEN=YANDEX_TOKEN,folder_id='b1gc4o0hrp0t5fgitmv0', target_language='en'):
    body = {
    "targetLanguageCode": target_language,
    "texts": text,
    "folderId": folder_id,
}

    headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {0}".format(IAM_TOKEN)
}

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
    json = body,
    headers = headers
)
    print(response.json())
    return response.json()['translations'][0]['text']

def preprocess(text):
    new_text = []


    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)

# task='sentiment'
# MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

tokenizer.save_pretrained(MODEL)
model.save_pretrained(MODEL)

tokenizer = AutoTokenizer.from_pretrained(MODEL)

labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"

with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
model.save_pretrained(MODEL)

text = "Good night 😊"
text = preprocess(text)
encoded_input = tokenizer(text, return_tensors='pt')
output = model(**encoded_input)
scores = output[0][0].detach().numpy()
scores = softmax(scores)

nlp = spacy.load("en_core_web_sm")

'''
If you get an error that it cannot find the model,
try at the command line
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm
'''

def text_tonality(input_txt, nlp=nlp, model=model,tokenizer=tokenizer):
    categorises = ['negative', 'neutral', 'positive']

    if detect(input_txt) != 'en':
        input_txt = translate(input_txt)

    text = preprocess(input_txt)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    max_index = np.argmax(scores)
    # scores_max = max(scores)
    # max_index = scores.index(scores_max)
    return categorises[max_index]

print(text_tonality("""its fuckin cool"""))
