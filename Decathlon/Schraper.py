import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('Decathlon_com_reviews.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'price', 'url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # loop through all pages
    for page in range(1,8):
        x = page * 32
        url = f'https://www.decathlon.nl/browse/c0-sporten/c1-wandelen/c2-rugzakken/_/N-25efpl?from={x}&size=32'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags = soup.find_all('div', {'class': 'product-block-top-main'})

        for tag in product_tags:
            name = tag.find('h2', {'class': 'vtmn-p-0'}).text.strip()
            price_tag = soup.find('span', {'class': 'vtmn-price'})
            price = price_tag.text.strip()            
            # url = tag.find('a', {'class': 'hit-area-listpage'})['href']
            # visit_url = f'https://www.bol.com{url}'
            # print(name)
            # writer.writerow({'name': name, 'price': price, 'url': url})
            writer.writerow({'name': name, 'price': price})