from csv import writer
import requests
import json
import os

outfile = "Output/Data"
storageList = []

# Create a directory to store the data
if not os.path.exists('Output'):
    os.makedirs('Output')

#======File managment=======
def BeverAPIWriteDataToJsonFile():
    with open(outfile+".json", 'w', encoding="utf8", newline="") as out:
        json.dump(storageList, out) 
        
def BeverAPIWriteDataToCSVFile():
    with open(outfile+".csv", 'w', encoding="utf8", newline="") as out:
        write = writer(out)
        write.writerow(["sku","rating","good points","bad points"])
    with open(outfile+".csv", 'a', encoding="utf8", newline="") as out:
        write = writer(out)
        for entry in storageList:
            write.writerow(entry)
            
            
#======Helpers==============

def appendToList(list, data):
    if(not data == None):
        list.append(data)
        
def BeverGetSKUNr(url:str):
    return url.split("-")[-1].split(".")[0]

#=====Main methods========
def BeverGetReviewsFromURL(url:str):
   skuNr = BeverGetSKUNr(url)
   request = requests.get("https://widgets.reevoo.com/api/product_reviews?per_page=3&trkref=BEV&sku="+skuNr+"&locale=nl-NL&display_mode=embedded&page=1")
   if(request.ok):
    data = json.loads(request.content)

    nrOfPages = int(data["body"]["pagination"]["total_pages"])
    
    for i in range(nrOfPages):
        data = BeverGetReviewFromURL(skuNr, i+1, outfile)
        if not data == None and not data in storageList:
            storageList.append(data)
         
def BeverGetReviewFromURL(skuNr, pagenr:int, outfile):
    request = requests.get("https://widgets.reevoo.com/api/product_reviews?per_page=3&trkref=BEV&sku="+skuNr+"&locale=nl-NL&display_mode=embedded&page="+str(pagenr))
    data = json.loads(request.content)
    data = data["body"]["reviews"]
    
    rating = []
    goodPoints = []
    badpoints = []
    
    for thingy in data:
        try:
            appendToList(rating, thingy["overall_score"])
        except:
            None
        try:
            appendToList(goodPoints, thingy["text"]["good_points"])
        except:
            None
        try:
            appendToList(badpoints, thingy["text"]["bad_points"])
        except:
            None
    if len(goodPoints) > 0 or len(badpoints > 0):
        return [skuNr,rating,goodPoints,badpoints]
    return None
    
# BeverGetReviewsFromURL("https://www.bever.nl/p/ayacucho-annapurna-softshell-B12AD90130.html?colour=4168")
