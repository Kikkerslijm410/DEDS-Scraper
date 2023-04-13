import csv
from threading import Thread
import time
from csv import writer
from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.common.by import By
import SchraperApi as BeverAPI
import os

url = "https://www.bever.nl/c/uitrusting/rugzakken/wandelrugzakken.html"
outputfile = 'Output/Beverbot.csv'
products = []
productNrs = []

# Create a directory to store the data
if not os.path.exists('Output'):
    os.makedirs('Output')

def getBrowser():
    ffoptions = Options()
    # ffoptions.add_argument("--headless")
    return webdriver.Firefox(options=ffoptions)    

def BeverInitialSetup(browser:webdriver.Firefox):
    browser.get(url)
    browser.find_element(By.ID, 'accept-all-cookies').click()
    element = browser.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div/div/div/div[8]/div/div/a[3]/span")
    pageAmount = element.get_attribute("textContent")
    print(pageAmount)
    return int(pageAmount)

def BeverLoadFindAllURLs(browser:webdriver.Firefox, baseurl):
    pageAmount = BeverInitialSetup(browser)
    url = baseurl
    links = []
    for i in range(pageAmount):
        url = baseurl+"?page="+str(i)
        links.extend(BeverGetURLFromPage(browser, url))
    return links
        
def BeverGetURLFromPage(browser:webdriver.Firefox, page):
    browser.get(page)
    URLS = []
    Products = browser.find_elements(By.XPATH, "//a[@class = 'as-a-link as-a-link--container as-m-product-tile__link']")
    
    for thing in Products:
        print(thing.get_attribute("href"))

    for element in Products:
        link = element.get_attribute("href")
        if(not "https://www.bever.nl" in link):
            URLS.append('https://www.bever.nl' + link)
        else:
            URLS.append(link)
    return URLS

def BeverGetProductData(browser:webdriver.Firefox, url):
    SkuNr = BeverAPI.BeverGetSKUNr(url)
    if(not SkuNr in productNrs):

        try:
            browser.get(url)
            try:
                browser.find_element(By.ID, 'accept-all-cookies').click()
            except:
                None
            #Get info
            
            brand = browser.find_element(By.XPATH, "//a[@class = 'as-a-link as-a-link--base']").text
            product = browser.find_element(By.XPATH, "//span[@class = 'as-a-text as-a-text--title']").text
            price = browser.find_element(By.XPATH, "//span[@data-qa = 'sell_price']").text.replace('€', '').replace(",",".")
            
            info = [SkuNr,brand, product, price]
            products.append(info)
            productNrs.append(SkuNr)
            BeverAPI.BeverGetReviewsFromURL(url)
        except:
            None

#=====================File Management==============================================
def writeToOutput(item):
    with open(outputfile, 'a', encoding="utf8", newline="") as out:
        write = writer(out)
        write.writerow(item)

def stringInOutput(item):
    with open(outputfile, 'r', encoding="utf8", newline="") as out:
        items = csv.reader(out, delimiter=",")
        for line in items:
            if item[1] in line[1] and item[2] == line[2]:
                print("IM WORKING!")
                return True
    return False

def setupOutputFile():
    with open(outputfile, 'w', encoding="utf8", newline="") as out:
        out.write("")

#=====================Threading====================================================
class MyThread(Thread):
    def __init__(self, name):
        """Initialize the thread"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        """Run the thread"""
        threadName = self.name
        threadNumber = int(threadName.split('#')[1]) #Convert the string containing the Thread name to a int for use in lists
        browser = getBrowser()
        while len(links) > 0:
            link = links.pop()
            BeverGetProductData(browser, link)
            print(threadName +" Finished "+ BeverAPI.BeverGetSKUNr(link))
        browser.close()

def create_threads():
    """
    Create a group of threads
    """
    for i in range(int(len(links)/50)): #Spawns a thread for each entry in a list threads (len(urls))
        name = "Thread #%s" % (i)
        my_thread = MyThread(name)
        my_thread.start()
    my_thread.join() 
    time.sleep(5)
    
    writeToOutput(["sku","brand","product","price"])
    for product in products:
        writeToOutput(product)
        
    BeverAPI.BeverAPIWriteDataToJsonFile()
    BeverAPI.BeverAPIWriteDataToCSVFile()
    print(len(productNrs))

if __name__ == "__main__":
    browser = getBrowser()
    global links
    setupOutputFile()
    links = BeverLoadFindAllURLs(browser, url)
    print(len(links))
    browser.close()
    create_threads()
    