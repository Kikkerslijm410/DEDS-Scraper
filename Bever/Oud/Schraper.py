import requests
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('bever_reviews.csv', 'w', newline='') as csvfile:
    fieldnames = ['name', 'price', 'url', 'review']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    driver = webdriver.Firefox()

    # loop through all pages
    for page in range(0,5):
        url = f'https://www.bever.nl/c/uitrusting/rugzakken/wandelrugzakken.html?size=48&page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        product_tags = soup.find_all('div', {'class': 'as-m-product-tile'})

        # loop through all products
        for tag in product_tags:
            name = tag.find('div', {'class': 'as-m-product-tile__title-wrapper'}).text.strip()
            price = tag.find('div', {'class': 'as-a-price__value as-a-price__value--sell'}).text.strip()
            url = tag.find('a', {'class': 'as-m-product-tile__link'})['href']
            visit_url = f'https://www.bever.nl{url}'

            # Ga naar de website om te kijken of er reviews zijn
            response = requests.get(visit_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            review_tags = soup.find_all('div', {'id': 'product_detail_tab_reviews'})
            
            # Kijk of er reviews zijn
            if not review_tags:
                continue

            # Navigeer naar de website
            driver.get(visit_url)

            # Klik op de knop om cookies te accepteren
            driver.find_element(By.ID, 'accept-all-cookies').click()

            # Vind de element door de ID te gebruiken en wacht tot het klikbaar is
            reviews_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "product_detail_tab_reviews")))

            # Klik op de knop om de pop-up met beoordelingen te openen
            reviews_button.click()
            
            # Scrape alle reviews en schrijf ze naar een csv file
            reviews = BeautifulSoup(driver.page_source, 'html.parser').find_all('span', {'class': 'as_lt'})

            for review in reviews:
                review_text = review.find_element_by_class_name("as-l-reviews__item-text").text.strip()
                writer.writerow({'name': name, 'price': price, 'url': visit_url, 'review': review_text})

    # Sluit de browser
    driver.quit()