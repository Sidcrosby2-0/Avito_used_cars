import requests
import cfscrape
from bs4 import BeautifulSoup
import re


def get_session():
    session = requests.Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0."
                      "0 YaBrowser/24.1.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru,en;q=0.9,es;q=0.8,la;q=0.7,pl;q=0.6",
        "Pragma": "no-cache",
        'dnt': '1',
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Access-Control-Allow-Origin": "*",
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site'
    }
    return cfscrape.create_scraper(sess=session)


url = 'https://www.avito.ru/all/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?f=ASgBAgICAkSGFMjmAfrwD~i79wI'

session = get_session()

response = session.get(url)
cookies = response.cookies.get_dict()
html = response.text
soup = BeautifulSoup(html, 'html.parser')
brands = []

response = session.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')
blocks = soup.find('div', class_=re.compile('popular-rubricator-links')).find_all('div',
                                                                     class_='popular-rubricator-row-xX6S9')

for block in blocks:
    brands.append(block.find('a', class_=re.compile('popular-rubricator-link')).get_text(strip=True))
