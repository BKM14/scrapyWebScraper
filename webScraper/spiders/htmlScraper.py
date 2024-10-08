import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import json
import time

with open('./webScraper/config.json', 'r') as f:
    config_file = json.load(f)


class HomeSpider(scrapy.Spider):
    name = "htmlScraper"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/'
    }

    start_urls = [
        "https://www.worldpharmanews.com/research-and-development",
        "https://pharmatimes.com/news/",
        "https://www.worldpharmaceuticals.net/news/",
        "https://health.economictimes.indiatimes.com/news/pharma",
        "https://pharmaceutical-journal.com/article/news/all",
        "https://www.biopharmadive.com/topic/pharma/"
    ]

    limit=50
    count={}

    def start_requests(self):
        for url in self.start_urls:
            baseURL = urlparse(url).netloc
            print(f"===========================================================================\n\n{baseURL.upper()}\n\n===========================================================================")
            
            URLType = config_file[baseURL]["type"]

            filename = baseURL + ".txt"
            textfile = open("./webScraper/data/htmlLinkFiles/" + filename, 'w')
            textfile.write("")
            textfile.close()

            if URLType == "dynamic":
                yield SeleniumRequest(url=url, callback=self.Selparse)
            else:
                self.count[baseURL] = 0
                yield scrapy.Request(url=url, callback=self.Normalparse, headers=self.headers)

    def Selparse(self, response, **kwargs):
        
        baseURL = urlparse(response.url).netloc

        path = Service(r"chromedriver-win64\chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=path, options=options)
        driver.get(response.url)
        timeDelay = config_file[baseURL]["delay"]
    

        for i in range(self.limit):
            next_button = driver.find_element(By.XPATH, config_file[baseURL]["next"])
            if next_button:
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(timeDelay)
        
        time.sleep(3)

        final_page = Selector(text=driver.page_source)

        self.extract_articles(final_page, baseURL)
        driver.quit()

    def Normalparse(self, response, **kwargs):

        baseURL = urlparse(response.url).netloc
        self.extract_articles(response,baseURL)
        next_button = response.xpath(config_file[baseURL]["next"]).getall()[-1]

        self.count[baseURL]+=1

        print("==============="+str(self.count[baseURL])+"=========="+str(response.url))

        if next_button is None:
            print("===============No more next button=========="+str(self.count[baseURL])+"=========="+str(response.url))

        if self.count[baseURL]<self.limit and next_button is not None:
            yield response.follow(next_button, callback = self.Normalparse)
        else:
            self.count[baseURL] = 0

    
    def extract_articles(self, response, baseURL):

        articles = response.xpath(config_file[baseURL]["article_path"]).getall()

        filename = baseURL + ".txt"
        textfile = open("./webScraper/data/htmlLinkFiles/" + filename, 'a')
        for tag in articles:
            textfile.write(tag + "\n")
        textfile.close()
        print("saved")

