from bs4 import BeautifulSoup
import numpy as np
import requests
from requests.models import MissingSchema
import trafilatura
from googlesearch import search

def beautifulsoup_extract_text_fallback(response_content):
    
    '''
    This is a fallback function, so that we can always return a value for text content.
    Even for when both Trafilatura and BeautifulSoup are unable to extract the text from a 
    single URL.
    '''
    
    # Create the beautifulsoup object:
    soup = BeautifulSoup(response_content, 'html.parser')
    
    # Finding the text:
    text = soup.find_all(text=True)
    
    # Remove unwanted tag elements:
    cleaned_text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',]

    # Then we will loop over every item in the extract text and make sure that the beautifulsoup4 tag
    # is NOT in the blacklist
    for item in text:
        if item.parent.name not in blacklist:
            cleaned_text += '{} '.format(item)
            
    # Remove any tab separation and strip the text:
    cleaned_text = cleaned_text.replace('\t', '')
    return cleaned_text.strip()
    

def extract_text_from_single_web_page(url):
    
    downloaded_url = trafilatura.fetch_url(url)
    try:
        text = trafilatura.extract(downloaded_url)
    except NameError and TypeError:
        try:
            resp = requests.get(url)
            # We will only extract the text from successful requests:
            if resp.status_code == 200:
                return beautifulsoup_extract_text_fallback(resp.content)
            else:
                # This line will handle for any failures in both the Trafilature and BeautifulSoup4 functions:
                return np.nan
        # Handling for any URLs that don't have the correct protocol
        except MissingSchema:
            return np.nan
    return text

def googlescrapper(query, n=10):

    '''
    Function to extract texts from n first pages from Google by query
    '''

    # Getting first 10 pages from Google search:
    urls = list(search(query, num_results=n))
    
    # Getting text from every web-page
    results = []
    for url in urls:
        text_ = extract_text_from_single_web_page(url)
        if isinstance(text_, str):
            text_ = text_.replace('\n','')
        results.append(text_)

    # Removing any web page that failed 
    cleaned_results = [text for text in results if str(text) != 'nan']

    return cleaned_results