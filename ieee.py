import requests
from bs4 import BeautifulSoup as BS

r = requests.get('https://www.ieee.org/publications/periodicals.html')
soup = BS(r.text, 'html.parser')

print(soup.prettify())   