import requests
from bs4 import *
# imports * imports all modules in a package

# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>

# <p class="story">Once upon a time there were three little sisters; and their names were
# <a target="_blank" href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a target="_blank" href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a target="_blank" href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>

# <p class="story">...</p>
# """

# soup = BeautifulSoup(html_doc, 'html.parser')
# print(soup.prettify())

# links = soup.find_all('a', class_='sister')
# for link in links:
#     print(link.get('href'))
#     print(link.get_text())

# quick exercise below------

response = requests.get("https://www.gutenberg.org/browse/scores/top")
soup = BeautifulSoup(response.text, 'html.parser')

heading = soup.find('h2', string='Top 100 EBooks yesterday')
book_list = heading.find_next('ol')
for book in book_list.find_all('li'):
    print(book.get_text())