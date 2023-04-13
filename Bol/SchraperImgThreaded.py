import os
import requests
import csv
from bs4 import BeautifulSoup
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Create a directory to store the downloaded images
if not os.path.exists('images'):
    os.makedirs('images')

lock = threading.Lock()

def get_images(start_page, end_page):
    with open('Bol_com_images.csv', 'w', newline='', encoding='utf-16') as csvfile:
        fieldnames = ['name', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for page in range(start_page,end_page+1):
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

                # Get the EAN code (loops through all the dt tags and checks if the text is EAN)
                for tag in soup.find_all('dt', {'class': 'specs__title'}):
                    if tag.text.strip() == 'EAN':
                        EANcode = tag.find_next_sibling('dd', {'class': 'specs__value'}).text.strip()
                
                print (EANcode)

                # Download the image and save it to a file (and in the directory we created earlier)
                image_response = requests.get(image)
                with open(f'images/{EANcode}.jpg', 'wb') as f:
                    f.write(image_response.content) 
                    # 1GB in porn........nah I got 1GB in backpacks images           
                
                try:
                    writer.writerow({'name': EANcode, 'url': visit_url})
                except UnicodeEncodeError:
                    print("Oopsie poopsie, I did a little woopsie")

threads = []
num_pages = 500
pages_per_thread = 500

for i in range(0, num_pages, pages_per_thread):
    start_page = i+1
    end_page = min(i+pages_per_thread, num_pages)
    t = threading.Thread(target=get_images, args=(start_page, end_page))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
