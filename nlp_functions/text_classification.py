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
    return response.json()['translations'][0]['text']

nlp = spacy.load("en_core_web_sm")

def semantic_classification(input_txt, nlp=nlp):
    if detect(input_txt) != 'en':
        input_txt = translate(input_txt)

    doc = nlp(text)
    filtered_tokens = [token for token in doc if not token.is_stop]
    filtered_tokens
    # lemmas = [
    # f"Token: {token}, lemma: {token.lemma_}"
    # for token in filtered_tokens
    # ]
    # lemmas


nlp = spacy.load("en_core_web_sm")

'''
Если вылетает ошибка, попробуйте в командной строке
python -m spacy download en_core_web_lg
'''
