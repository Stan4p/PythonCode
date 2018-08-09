from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import requests
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import re


def get_html(url):
    chrome_options = Options() 
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/Users/stanislavpresnyakov/Documents/chromedriver')  
    driver.get(url)
    r = driver.page_source
    driver.close()
    return r

def get_all_cat_links(html):
    soup = BeautifulSoup(html, 'lxml')
    links_all = []
    blocks = soup.find_all('tr', class_ = 'cr-desc-tr')
    for block in blocks:
        categs = block.find_all('ul', class_ = 'cr-section-categories')
        for categ in categs:
            links = categ.find_all('li')
            for link in links:
                try:
                    true_link = link.find('a').get('href')
                except:
                    true_link = '#'
                if true_link != '#':
                    links_all.append(true_link)
    return links_all

def get_first_links():
    # soup = BeautifulSoup(html, 'lxml')
    # links = []
    # cats = soup.find('ul', class_ = 'catalog-left-menu').find_all('li')
    # for cat in cats:
    #     link = cat.find('a').get('href')
    #     if link != '/catalogue/predlozhenie-ogranicheno/':
    #         links.append('https://perm.leroymerlin.ru' + link)
    links = ['https://perm.leroymerlin.ru/catalogue/stroymaterialy/',]

    return links

def write_csv(data):
    with open('leroi.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['catalog'],data['name'], data['price']))

def make_all(link):
    html = get_html(link)
    soup = BeautifulSoup(html, 'lxml')
    try:
        ads = soup.find('ul', class_ = 'catalog').find_all('li', class_ ='catalog__item')
        for ad in ads:
            try:
                name = ad.find('div', class_ = 'catalog__desc').find('p', class_ = 'catalog__name').find('a').text.strip()
            except:
                name = ''
            try:
                price_text = ad.find('div', class_ = 'catalog__desc').find('p', class_ = 'catalog__price').text
                price = re.match(r'\d?\d? ?\d+,\d{2}', price_text).group()
            except:
                price = ''
            try:
                catalog = soup.find('div', class_ = 'catalog__partition_title').find('h1').text
            except:
                catalog = ''

            data = {'catalog' : catalog,
                    'name': name,
                    'price': price}
            if data.get('name') != '':
                write_csv(data)
    except:
        pass
    print(link , 'DONE')


def get_all_links(links):
    all_links = []
    for link in links:
        html = get_html(link)
        end_links = get_all_cat_links(html)
        for end_link in end_links:
            all_links.append('https://perm.leroymerlin.ru' + end_link)
    print('get_all_links DONE')
    return(all_links)

def main():
    #first_url = 'https://perm.leroymerlin.ru/catalogue/'
    #first_page = get_html(first_url)
    links = get_first_links()
    all_links = get_all_links(links)
    print(len(all_links))
    s = 1
    for link in all_links:
        print(s, end = ' ')
        make_all(link)
        s += 1



        # html = get_html(url)
        # get_page_data(html)


if __name__ == '__main__':
    main()