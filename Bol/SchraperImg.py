import os
import requests
import csv
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Create a directory to store the downloaded images
if not os.path.exists('images'):
    os.makedirs('images')

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
            url = tag.find('a', {'class': 'hit-area-listpage'})['href']
            
            visit_url = f'https://www.bol.com{url}'
            response = requests.get(visit_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            image = soup.find('img', {'class': 'js_selected_image'})['src']
            EANcode = soup.find_all('dd', {'class': 'specs__value'})[7].text.strip() 
            
            # Download the image and save it to a file
            image_response = requests.get(image)
            with open(f'images/{EANcode}.jpg', 'wb') as f:
                f.write(image_response.content)
            # needs a uniqe code without / and spaces
            
            print (EANcode)
            
            try:
                writer.writerow({'name': name, 'url': visit_url, 'image': image})
            except UnicodeEncodeError:
                print("Oopsie poopsie, I did a little woopsie")
