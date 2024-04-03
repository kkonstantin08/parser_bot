# schedule
import time

# import schedule
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import requests
import os

url = 'https://www.wildberries.ru/catalog/78504395/detail.aspx'


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

    price1 = (content.find('span', {'class': 'price-block__wallet-price'}).text.split())[0]
    price2 = (content.find('ins', {'class': 'price-block__final-price wallet'}).text.split())[0]
    title = content.find('h1', {'class': 'product-page__title'}).text
    # img = content.find('img', {'class': 'product-zoom__preview'})
    # file = open(title + '.png', 'wb')
    # file.write(requests.get(img).content)
    # file.close()

    print(price1, price2, title)


func()
# schedule.every().day.at('14:40').do(func)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


# images = soup.find_all('img')
# # Проверяем, есть ли хотя бы одно изображение
# if images:
#     image_url = images[0]['src']  # Берем URL первого изображения
#
#     # Если URL изображения является относительным, добавляем базовый URL
#     if not image_url.startswith('http'):
#         image_url = os.path.join(url, image_url)
#
#     image_data = requests.get(image_url).content  # Загружаем данные изображения
#
#     with open('image.jpg', 'wb') as handler:  # Записываем данные изображения в файл
#         handler.write(image_data)
# else:
#     print("На странице нет изображений.")
