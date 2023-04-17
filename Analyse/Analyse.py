import csv

with open('Analyse/reviews.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader) # skip the header row
    for row in reader:
        # Change the index to match the column you want to extract
        reviewGood = row[2]

        # perform word count
        word_countG = len(reviewGood.split())
        
        # print the results
        print(f'Review: {reviewGood}')
        print(f'Word count: {word_countG}\n')
