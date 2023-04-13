import math
import time
import os
import requests
import csv
import json
from bs4 import BeautifulSoup
import traceback

from os.path import basename

from colorama import Fore, Back, Style

url = "https://www.decathlon.nl/browse/c0-sporten/c1-wandelen/c2-rugzakken/_/N-25efpl"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
}

# Create a directory to store the data
if not os.path.exists('Output'):
    os.makedirs('Output')

# Create a directory to store the data
if not os.path.exists('Images2'):
    os.makedirs('Images2')

MIN_REVIEW_LENGTH = 0
REVIEW_LANGUAGE = 'en'
TRIES = 3
FILENAME = 'Output/Decathlon_review.csv'
PICS_FOLDER = 'Images2'

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

plp_bar_info = soup.find('div', class_='plp-bar-info')
plp_tag = plp_bar_info.find('span', class_='vtmn-tag')

amount_of_products = int(plp_tag.text)

print(amount_of_products)

amount_of_pages = math.ceil(amount_of_products / 32)
print(amount_of_pages)

with open(FILENAME, 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ['productcode', 'review_id', 'review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


def get_product_code(product_url):
    print(product_url)
    product_url_parts = product_url.split('mc=')[1]
    product_code = product_url_parts.split('&')[0]
    return product_code


def get_product_reviews(product_code, product_url):
    product_url_response = requests.get(product_url, headers=headers)
    product_url_soup = BeautifulSoup(product_url_response.content, 'html.parser')
    slide_section = product_url_soup.find('section', class_='slide')
    img = slide_section.find('img', src=True)
    product_image = img['src']
    print(product_image)

    review_url_format = 'https://www.decathlon.nl/nl/ajax/nfs/reviews/{}?page={}&count=20'
    review_url = review_url_format.format(product_code, 1)
    for a in range(0, TRIES):
        try:
            review_response = requests.get(review_url, headers=headers)
            review_json = json.loads(review_response.text)
            stats = review_json['stats']
            reviewsCount = stats['reviewsCount']
            print(">> Aantal reviews: " + str(reviewsCount))
            pages = math.ceil(reviewsCount / 20)
            print(">> Aantal pagina's: " + str(pages))

            for i in range(0, pages):
                for j in range(0, TRIES):
                    try:
                        review_url = review_url_format.format(product_code, i + 1)
                        review_response = requests.get(review_url, headers=headers)
                        review_json = json.loads(review_response.text)
                        reviews = review_json['reviews']
                        for review in reviews:
                            review_id = review['reviewId']
                            review_text = review['review']
                            body = review_text['body']
                            body = body.replace('<br>', ' ')
                            body = body.replace('<br />', ' ')
                            aantal_woorden = len(body.split())
                            if aantal_woorden >= MIN_REVIEW_LENGTH and review_text['locale'] == REVIEW_LANGUAGE:
                                print(Fore.GREEN + ">>>> Review met ID: " + str(review_id) + " en " + str(aantal_woorden) + " woorden")
                                print(Style.RESET_ALL)
                                filename = basename(product_image).split("?")[0].split(".jpg")[0] + "_" + str(product_code) + ".jpg"
                                print(">>>> Bestandsnaam van de afbeelding: " + PICS_FOLDER + "/" + filename)
                                with open(PICS_FOLDER + '/' + filename, 'wb') as handle:
                                    response = requests.get(product_image, stream=True)
                                    if not response.ok:
                                        print(response)
                                    for block in response.iter_content(1024):
                                        if not block:
                                            break
                                        handle.write(block)
                                with open(FILENAME, 'a', newline='', encoding="utf-8") as csvfile:
                                    fieldnames = ['productcode', 'review_id', 'review']
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writerow({'productcode': product_code, 'review_id': review_id, 'review': body})
                        break
                    except:
                        print(">> Er ging iets mis bij het ophalen van de reviews op url: " + review_url)
                        if j == TRIES - 1:
                            print(Fore.RED + ">> Geen reviews gevonden voor product: " + product_code + "op url: " + review_url)
                            print(Style.RESET_ALL)
                            traceback.print_exc()
                            return
                        if j < TRIES:
                            print(Fore.BLUE + ">> Nogmaals proberen... (poging " + str(j + 2) + "/" + str(TRIES) + ")")
                            print(Style.RESET_ALL)
                            time.sleep(3)
            break
        except:
            print(">> Geen reviews gevonden voor product: " + product_code + "op url: " + review_url)
            if a == TRIES - 1:
                print(Fore.RED + ">> Geen reviews gevonden voor product: " + product_code + "op url: " + review_url)
                print(Style.RESET_ALL)
                traceback.print_exc()
                return
            if a < TRIES:
                print(Fore.BLUE + ">> Nogmaals proberen... (poging " + str(a + 2) + "/" + str(TRIES) + ")")
                print(Style.RESET_ALL)
                time.sleep(3)


for i in range(0, amount_of_pages):
    print(i)
    from_index = i * 32
    size = 32
    url = "https://www.decathlon.nl/browse/c0-heren-sportkleding/c1-jassen-heren/_/N-1darl2t?from={}&size={}"
    url = url.format(from_index, size)
    print(url)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_list = soup.find('div', class_='product-list')
    links = product_list.find_all('a', href=True, class_='dpb-product-model-link')
    for link in links:
        # print("https://www.decathlon.nl" + link['href'])
        product_code = get_product_code("https://www.decathlon.nl" + link['href'])
        get_product_reviews(product_code, "https://www.decathlon.nl" + link['href'])

    names = product_list.find_all('span', class_='vh')
    for name in names:
        print(name.text)
