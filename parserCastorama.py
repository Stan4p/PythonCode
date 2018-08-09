import requests
import csv
from bs4 import BeautifulSoup

def get_html(url):
    r = requests.get(url)
    return r.text

def write_csv(data):
    with open('castorama.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['price']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('ul', class_ = 'products-grid').find_all('li', class_ = 'item')
    for ad in ads:
        name = ad.find('div', class_ = 'product-info').find('div', class_ = 'product-name').text
        price = ad.find('div', class_ = 'price-wrapper').find('div', class_ = 'price-box').text.strip()
        data = {'name': name,
                'price': price}
        write_csv(data)

def main():
    base_url = 'https://www.castorama.ru/building-materials/building-dry-materials-and-primers/'

    parts = ['plasters', 'fillers', 'floor-screeds-and-self-leveling', 'adhesive-for-tiles', 'laying-mortars', ]
    for part in parts:
        url = base_url + part + '?limit=96'
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()