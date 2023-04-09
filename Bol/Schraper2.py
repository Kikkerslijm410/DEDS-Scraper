import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('Bol_com_reviews.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'price', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # loop through all pages
    for page in range(1,5):
        url = f'https://www.bol.com/nl/nl/l/rugzakken/20701/?page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags = soup.find_all('li', {'class': 'product-item--column'})

        for tag in product_tags:
            name = tag.find('span', {'class': 'truncate'}).text.strip()
            price = soup.find('meta', {'itemprop': 'price'})['content']
            url = tag.find('a', {'class': 'hit-area-listpage'})['href']
            visit_url = f'https://www.bol.com{url}'
            print(name)
            writer.writerow({'name': name, 'price': price, 'url': url})
