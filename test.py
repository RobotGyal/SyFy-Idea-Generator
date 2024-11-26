import os
import requests
import json
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

start_time = datetime.now()

parent_genre_url = 'https://www.goodreads.com/genres'

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
genre_div = genre_soup.find_all('div',class_="rightContainer")

base_url = 'https://www.goodreads.com/'


genre_url_list = []
for child_div in genre_div:
    subchild_div = child_div.find_all('div', class_='left')
    for left_tag in subchild_div:
       a_tag = left_tag.find_all('a')
       for h_ref in a_tag:
            sub_directory = h_ref.get('href')
            split_list = sub_directory.split('/')
            final_url = base_url + split_list[1] + '/' + 'most_read' + '/' + split_list[2]
            genre_url_list.append(final_url)

genre_url_list = genre_url_list[0:3] # only 3 genres to test

book_url_list = []
for genre_url in genre_url_list:
    book_list_soup = get_soup(genre_url)
    book_list_div = book_list_soup.find_all('div', class_="leftAlignedImage bookBox")

    for book_url_div in book_list_div:
        try:
            book_url_full = book_url_div.find('a')['href']
            book_url = base_url + book_url_full
            book_url_list.append(book_url)
        except TypeError:
            pass

book_url_list_len = len(book_url_list)
print(f"Book url list is {book_url_list_len} items long")

def book(book_url):
    book_soup = get_soup(book_url)
    try:
        book_div = book_soup.find('script', type="application/ld+json")
    except AttributeError:
        book_div = "None"
    try:
        publish_div = book_soup.find("div", class_="BookDetails").find("div", class_="FeaturedDetails").find_all("p")
    except AttributeError:
        publish_div = 'None'
    try: 
        genre_div = book_soup.find("div", class_ ="BookPageMetadataSection__genres").find("span", class_ ="BookPageMetadataSection__genreButton")
    except AttributeError:
        genre_div = 'None'


    try:
            script_json = json.loads(book_div.string)
            title = script_json['name']
            author = script_json['author'][0]['name']
            no_pages = script_json['numberOfPages']
            rating_count = script_json['aggregateRating']['ratingCount']
            average_rating =  script_json['aggregateRating']['ratingValue']
            review_count = script_json['aggregateRating']['reviewCount']
            isbn = script_json['isbn']
    except (TypeError,KeyError,AttributeError,IndexError):
            title = ""
            author = ""
            no_pages = ""
            rating_count = ""
            average_rating = ""
            review_count = ""
            isbn = ""

    try:
            publish_date = publish_div[1].text.split("First published")[1].strip()
    except (TypeError,KeyError,AttributeError,IndexError):
            publish_date = ""

    try:
            genre = genre_div.text
    except (TypeError,KeyError,AttributeError,IndexError):
            genre = ""


        
    book_dict = {
            "Title": title, 
            "Author": author,
            "Genre": genre,
            "NumberOfPages": no_pages,
            "PublishDate": publish_date,
            "Rating Count": rating_count,
            "Average_Rating": average_rating,
            "Review Count": review_count,
            "ISBN": isbn
        }

    return book_dict

book_list = []
for book_url in book_url_list:

    book_dict = book(book_url)
    #print(book_dict)
    book_list.append(book_dict)

book_list_len = len(book_list)
print(f"Book list is {book_list_len} items long")

df = pd.DataFrame(book_list)

end_time = datetime.now()
duration = end_time - start_time

print(f"Script runtime: {duration}")
print(df)

# saving the dataframe
df.to_csv('test_file.csv')