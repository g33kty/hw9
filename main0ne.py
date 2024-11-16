from bs4 import BeautifulSoup
import requests
import json

url = 'http://quotes.toscrape.com'
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, 'lxml')
quotes = soup.find_all('div', class_='quote')


authors_json = list()
quotes_json = list()
i = 0
for quote in quotes:
    text = quote.find('span', class_='text').get_text()
    author = quote.find('small', class_='author').get_text()
    tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]

    author_url_tag = quote.find('a', href=True)
    paths_for_authors = url + author_url_tag['href']
    response = requests.get(paths_for_authors)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'lxml')
    sub_author = soup.find("h3", class_='author-title')
    born_date = soup.find("span", class_='author-born-date')
    born_location = soup.find("span", class_='author-born-location')
    description = soup.find("div", class_='author-description')

    temp = dict()
    temp["fullname"] = sub_author.text
    temp["born_date"] = born_date.text
    temp["born_location"] = born_location.text
    temp["description"] = description.text[9:]
    authors_json.append(temp)

    temp2 = dict()

    temp2["tags"] = tags
    temp2["author"] = author
    temp2["quote"] = text
    quotes_json.append(temp2)
    i+=1
    print(f"got {i}")

with open('authorsHW.json', 'w', encoding='utf-8') as json_file:
    json.dump(authors_json, json_file, ensure_ascii=False, indent=2)
with open('quotesHW.json', 'w', encoding='utf-8') as json_file:
    json.dump(quotes_json, json_file, ensure_ascii=False, indent=2)
