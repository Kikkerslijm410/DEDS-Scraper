import os
import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('Bol_com_reviews.csv', 'w', newline='', encoding='utf-16') as csvfile:
    fieldnames = ['name', 'price', 'url', 'image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for page in range(1,500):
        print ('huidige pagina: ' + str(page))
        url = f'https://www.bol.com/nl/nl/l/rugzakken/20701/?page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags = soup.find_all('li', {'class': 'product-item--column'})

        for tag in product_tags:
            name = tag.find('span', {'class': 'truncate'}).text.strip()
            price = soup.find('meta', {'itemprop': 'price'})['content']
            image = soup.find('img', {'class': 'js_product_image'})['src']
            url = tag.find('a', {'class': 'hit-area-listpage'})['href']
            visit_url = f'https://www.bol.com{url}'
            print(name)

            try:
                writer.writerow({'name': name, 'price': price, 'url': visit_url, 'image': image})
            except UnicodeEncodeError:
                print("Oopsie poopsie, I did a little woopsie")
