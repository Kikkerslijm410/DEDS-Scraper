import csv

with open('OutputOld/Reviews2.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader) # skip the header row
    for row in reader:
        # Change the index to match the column you want to extract
        review = row[1]

        # perform word count
        word_countG = len(review.split())
        
        # print the results
        print(f'Review: {review}')
        print(f'Word count: {word_countG}\n')
