import requests
from bs4 import BeautifulSoup
import json

# URL страницы товара
url = 'https://www.wildberries.ru/catalog/8707379/detail.aspx'

# Отправляем запрос на страницу
response = requests.get(url)

# Парсим HTML страницу
soup = BeautifulSoup(response.text, 'html.parser')

# Извлекаем данные о товаре
product_data = []
for product in soup.find_all('div', class_='dtList i-dtList j-card-item'):
    title = product.find('strong', class_='brand-name').text
    price = product.find('ins', class_='lower-price').text
    old_price = product.find('del', class_='c-text-base').text if product.find('del', class_='c-text-base') else None
    discount = product.find('span', class_='sale').text if product.find('span', class_='sale') else None

    product_data.append({
        'title': title,
        'price': price,
        'old_price': old_price,
        'discount': discount
    })

# Преобразуем данные в JSON
json_data = json.dumps(product_data, ensure_ascii=False)

print(json_data)
