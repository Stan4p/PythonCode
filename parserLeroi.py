from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import requests
import csv
from bs4 import BeautifulSoup

def get_html(url):
    chrome_options = Options() 
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/Users/stanislavpresnyakov/Documents/chromedriver')  
    driver.get(url)
    r = driver.page_source
    driver.close()
    return r

def write_csv(data):
    with open('leroi.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'], data['price']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('ul', class_ = 'catalog').find_all('li', class_ ='catalog__item')
    for ad in ads:
        try:
            name = ad.find('div', class_ = 'catalog__desc').find('p', class_ = 'catalog__name').find('a').text.strip()
        except:
            name = ''
        try:
            price = ad.find('div', class_ = 'catalog__desc').find('p', class_ = 'catalog__price').text
        except:
            price = ''
        
        data = {'name': name,
                'price': price}
        write_csv(data)


def main():
    base_url = 'https://perm.leroymerlin.ru/catalogue/'

    parts = ['shtukaturki', 'shpaklevki', 'suhie-smesi-dlya-pola', 'montazhnye-i-kladochnye-smesi', 'sypuchie-materialy-cement-pesok-keramzit', 'klei-dlya-plitki-kamnya-i-izolyacii']
    for part in parts:
        url = base_url + part
        get_page_data(get_html(url))

if __name__ == '__main__':
    main()