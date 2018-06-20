# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

#Grab the html content
response = requests.get('https://www.michigandaily.com/')
soup = BeautifulSoup(response.text, 'html.parser')

#parse through it
most_read = soup.find('div', class_='panel-pane pane-mostread')
articles = most_read.find_all("a")
article_names = []
article_links = []
for article in articles:
    article_names.append(article.text)
    article_links.append("http://www.michigandaily.com" + article.get('href'))
authors = []
for article in article_links:
    request2 = requests.get(article)
    more_soup = BeautifulSoup(request2.text, 'html.parser')
    try:
        author = more_soup.find('div', class_='byline').find_next('a').text
        authors.append(author)
    except:
        authors.append("DAILY STAFF WRITER")

#print it all out
print("Michigan Daily -- MOST READ")
for i in range(0, len(article_names)):
    print(article_names[i])
    print("  by " + authors[i])
