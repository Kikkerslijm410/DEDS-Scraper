import pandas as pd
import requests
import re
import os

# so much code for so little results
response = requests.get("https://www.scoutshop.nl/backpacks-en-tassen/tassen?product_list_limit=all")

answer = re.findall('data-product-id=\"(.+?)\"', response.text)

reviews = []
waardering = []
productid = []
wordcount = []

# Create a directory to store the data
if not os.path.exists('Output'):
    os.makedirs('Output')

for prodid in answer:
    response2 = requests.get("https://www.scoutshop.nl/review/product/listAjax/id/"+prodid)

    reviews = re.findall('<div class="review-content" itemprop="description">(.+?)</div>' , response2.text, re.S)

    print(prodid)
    for review in reviews:
        review = re.sub('<br/>','', review)
        review = re.sub('<br />','', review)
        productid.append(prodid)
        waardering.append(review.strip())
        wordcount.append(len(review.split()))
        print("-----------------------------")
        print(review)

data = {"ProductID": productid,
        "ReviewText": waardering,
        "Wordcount":wordcount}
df = pd.DataFrame(data)
df.to_csv("ScoutShop_reviews.csv", index=False)