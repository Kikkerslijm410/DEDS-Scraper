import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('Decathlon_com_reviews.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['name', 'review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for page in range(1, 8):
        x = page * 32
        url = f'https://www.decathlon.nl/browse/c0-sporten/c1-wandelen/c2-rugzakken/_/N-25efpl?from={x}&size=32'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags = soup.find_all('div', {'class': 'product-block-top-main'})

        for tag in product_tags:
            name = tag.find('h2', {'class': 'vtmn-p-0'}).text.strip()
            url = tag.find('a', {'class': 'dpb-product-model-link'})['href']
            
            visit_url = f'https://www.decathlon.nl{url}'
            response2 = requests.get(visit_url)
            review_soup = BeautifulSoup(response2.content, 'html.parser')
            review_tags = review_soup.find_all('p', {'class': 'answer-body'})

            for review_tag in review_tags:	
                review = review_tag.text.strip()
                writer.writerow({'name': name, 'review': review})

