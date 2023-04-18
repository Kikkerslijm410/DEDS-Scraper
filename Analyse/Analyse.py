import csv

with open('OutputOld/Reviews.csv', newline='', encoding='utf-16') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader) # skip the header row
    review_count = 0
    for row in reader:
        # Change the index to match the column you want to extract
        review = row[1]

        # perform word count
        word_countG = len(review.split())
        
        # print the results
        print(f'Review: {review}')
        print(f'Word count: {word_countG}\n')
        review_count += 1
    
    print(f'Total reviews: {review_count}')
