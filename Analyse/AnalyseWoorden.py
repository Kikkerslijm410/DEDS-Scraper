import csv
from collections import defaultdict
import re
from Database import (drop_table,create_table,insert_word)

table_name = "PopularWords"
drop_table(table_name)
print ("INFO: Table dropped")
create_table(table_name, "word","count")
print ("INFO: Table 'PopularWords' created")

# create a defaultdict to keep track of word counts
words_with_count = defaultdict(int)

with open('Analyse/reviews.csv', newline='', encoding='utf-16') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader) # skip the header row
    for row in reader:
        # extract the review title from the row
        title = row[2]
        # remove any non-letter characters, except spaces
        title = re.sub(r'[^a-zA-Z\s]', '', title)
        # split the title into individual words
        words = title.split()
        # iterate over each word in the title and increment its count in the defaultdict
        for word in words:
            words_with_count[word] += 1
for word in words_with_count:
    insert_word(table_name,word, words_with_count[word])
print("Analysis has been completed and the analyzed data has been saved in the database.")
