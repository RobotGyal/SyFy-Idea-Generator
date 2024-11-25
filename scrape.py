import os
import requests
import json
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

start_time = datetime.now()

parent_genre_url = 'https://www.goodreads.com/shelf/show/science-fiction'

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    response = requests.get(f"{url}", headers=headers)
    response = response.text
    soup = BeautifulSoup(response, 'lxml')
    return soup

# lxml =  0:07:35.762512
# html5 = 0:09:41.541314
# html.parser = 0:08:14.770100

genre_soup = get_soup(parent_genre_url)
genre_div = genre_soup.find_all('div',class_="leftContainer")

base_url = 'https://www.goodreads.com/'