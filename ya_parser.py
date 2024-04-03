# import schedule
import time

from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import requests
import os



url = 'https://market.yandex.ru/product--ua31/1776686124?sku=101850335793&uniqueId=13433419&do-waremd5=9WkuUZbK7Aj4PFj2XvFg_g'


# options = Options()
# options.add_argument('--headless')
# browser = wd.Chrome(options=options)
# browser.get(url)
def func():
    global url
    # options = Options()
    # options.add_argument('--headless')
    browser = wd.Chrome()
    browser.get(url)

    time.sleep(3)

    content = BeautifulSoup(browser.page_source, 'lxml')

    price1 = (content.find('h3', {'class': 'Jdxhz'}).text.split())[4][4:]
    price2 = (content.find('span', {'class': '_2r9lI'}).text.split())
    title = content.find('h1', {'class': '_3TVFy _2SUA6 jM85b _13aK2 _1A5yJ'}).text
    # img = content.find('img', {'class': 'product-zoom__preview'})
    # file = open(title + '.png', 'wb')
    # file.write(requests.get(img).content)
    # file.close()

    print(price1, title, price2[2], price2[3][1:])
    browser.quit()

func()

