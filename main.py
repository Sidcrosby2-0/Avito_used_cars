import requests
import cfscrape
from bs4 import BeautifulSoup
import pandas as pd
import re
from carsList import brands
import time
import random


def brand_split(name):
    name = name.split('.')
    name = name[0]
    name = name[:-2]
    name = name.split(' ')
    if len(name) == 2:
        brand = name[0]
    elif len(name) == 4:
        brand = name[0] + ' ' + name[1]
    elif len(name) == 3:
        if name[0] + ' ' + name[1] in brands:
            brand = name[0] + ' ' + name[1]
        else:
            brand = name[0]
    elif len(name) == 5:
        if name[0] + ' ' + name[1] + ' ' + name[2] in brands:
            brand = name[0] + ' ' + name[1] + ' ' + name[2]
        else:
            brand = name[0] + ' ' + name[1]

    return brand


def model_split(name):
    name = name.split('.')
    name = name[0]
    name = name[:-2]
    name = name.split(' ')
    if len(name) == 2:
        model = name[1]
    elif len(name) == 4:
        model = name[2] + ' ' + name[3]
    elif len(name) == 3:
        if name[0] + ' ' + name[1] in brands:
            model = name[2]
        else:
            model = name[1] + ' ' + name[2]
    elif len(name) == 5:
        if name[0] + ' ' + name[1] + ' ' + name[2] in brands:
            model = name[3] + ' ' + name[4]
        else:
            model = name[2] + ' ' + name[3] + ' ' + name[4]

    return model


def year_split(name):
    year = name.split(',')[1]
    year = year[1:]
    return year


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
print(soup.h1.text)
pagination = soup.find('div', class_='js-pages pagination-pagination-_FSNE').find_all('li')
pages_all = pagination[-2].text
print(f'Найдено {pages_all} страниц')
pages = (input('Сколько страниц просматривать? '))
if pages.lower() == 'все' or pages.lower() == 'all':
    pages = pages_all
else:
    pages = int(pages)
data = []
for page in range(1, int(pages) + 1):
    response = session.get(url, params={'&p': page})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find('div', class_=re.compile('items-items')).find_all('div',
                                                                         class_='iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum')
    print(f'Парсинг страницы {page} из {pages}...')

    for block in blocks:
        for block in blocks:
            data.append({
                'Заголовок': block.find('h3', class_=re.compile('styles-module-root')).get_text(strip=True),
                'Объём двигателя':
                    block.find('div', class_=re.compile('iva-item-autoParamsStep')).get_text(strip=True).split(' ')[1],
                'Пробег': block.find('div', class_=re.compile('iva-item-autoParamsStep')).get_text(strip=True).replace
                ('\xa0', '').replace('км', '').replace(',', '').split(' ')[0],
                'Привод':
                    block.find('div', class_=re.compile('iva-item-autoParamsStep')).get_text(strip=True).replace
                    (',', '').split(' ')[5],
                'Тип ДВС':
                    block.find('div', class_=re.compile('iva-item-autoParamsStep')).get_text(strip=True).split(' ')[
                        6],
                'Мощность': block.find('div', class_=re.compile('iva-item-autoParamsStep')).get_text(strip=True).replace
                ('\xa0л.с.)', '').replace('(', '').replace(',', '').split(' ')[3],
                'Тип КПП':
                    block.find('div', class_=re.compile('iva-item-autoParamsStep')).get_text(strip=True).split(' ')[
                        2],
                'Цена': block.find('strong', class_=re.compile('styles-module-root-LIAav')).find('span').get_text(
                    strip=True).replace('\xa0', '').replace('₽', '')
            })
    time.sleep(random.randint(5, 10))

print(f'Найдено {len(data)} товаров')
print(f'Простмотрено {pages} страниц')

df = pd.DataFrame(data)
df['Марка'] = df['Заголовок'].apply(brand_split)
df['Модель'] = df['Заголовок'].apply(model_split)
df['Год выпуска'] = df['Заголовок'].apply(year_split)
df = df[['Марка', 'Модель', 'Год выпуска', 'Пробег', 'Объём двигателя', 'Тип ДВС', 'Мощность', 'Тип КПП', 'Привод', 'Цена']]
df.to_csv('avito_pars.csv', index=False)
