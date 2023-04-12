import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('Bol_com_reviews.csv', 'w', newline='', encoding='utf-16') as csvfile:
    fieldnames = ['name', 'review', 'image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for page in range(1, 500):
        print('huidige pagina: ' + str(page))
        url = f'https://www.bol.com/nl/nl/l/rugzakken/20701/?page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_tags = soup.find_all('li', {'class': 'product-item--column'})

        for tag in product_tags:
            name = tag.find('span', {'class': 'truncate'}).text.strip()
            url = tag.find('a', {'class': 'hit-area-listpage'})['href']
            print (url)
            
            visit_url = f'https://www.bol.com{url}'
            response = requests.get(visit_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            image = soup.find('img', {'class': 'js_selected_image'})['src']
            review_tags = soup.find_all('div', {'class': 'review__body'})

            for review_tag in review_tags:
                review = review_tag.text.strip()
                try:
                    writer.writerow({'name': name, 'review': review.replace('\uFFFD', ''), 'image': image.replace('\uFFFD', '')})
                except UnicodeEncodeError:
                    print("Oopsie poopsie, I did a little woopsie")