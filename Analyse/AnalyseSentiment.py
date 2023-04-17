import csv
import re
import json
import matplotlib.pyplot as plt
from Database import (drop_table,conn,cursor,create_table)

table_name = "SentimentAnalyse"
drop_table(table_name)
print ("INFO: Table dropped")
create_table(table_name, "type","total")
print ("INFO: Table 'SenitmentAnalyse' created")

def insert_data(type, total ):
    cursor.execute(f"INSERT INTO {table_name} (type, total) VALUES (?, ?)", type, total)
    print(f"{type} reviews: {total} (saved in database)")
    conn.commit()
    
# Load word list from json file
def get_word_list(category):
    with open(category + '.json', 'r') as f:
        word_list = json.load(f)
    return word_list

# Determine sentiment of a review
def get_sentiment(review):
    review = re.sub('[^\w\s]', '', review).lower()
    positive_words = get_word_list('Analyse/Woorden/Positive')
    negative_words = get_word_list('Analyse/Woorden/Negative')
    words = review.split()
    positive_count = 0
    negative_count = 0
    for word in words:
        if word[:-1] in [w.lower() for w in positive_words] or word in [w.lower() for w in positive_words]:
            positive_count += 1 
        elif word in [w.lower() for w in negative_words] or word[:-1] in [w.lower() for w in negative_words]:
            negative_count += 1
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

# Initialize sentiment counter
reviews_sentiment = {"positive": 0, "negative": 0, "neutral": 0 }

with open('OutputOld/Reviews.csv', newline='', encoding='utf-16') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader) # skip the header row
    for row in reader:
        if row[1]:    
            print (row[1])
            sentiment = get_sentiment(row[1])
            reviews_sentiment[sentiment] += 1

# Print sentiment counts
for sentiment in ['negative', 'neutral', 'positive']:
    insert_data(sentiment, reviews_sentiment[sentiment])

# Plot sentiment bar chart
left = [1, 2, 3]
tick_label = ['Negative', 'Neutral', 'Positive']
plt.bar(left, height=(reviews_sentiment['negative'],reviews_sentiment['neutral'],reviews_sentiment['positive']), 
        tick_label=tick_label, width=0.8, color=( "#FA332D","#3E3F3F","#06B076"))
plt.title('Customer Satisfaction Statistics')
plt.show()