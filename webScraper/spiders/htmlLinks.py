import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

class LinksSpider(scrapy.Spider):
    name = "htmlLinks"
    count = 0
    start_urls = [
        "https://www.fiercepharma.com/",
        "https://www.worldpharmanews.com/",
        "https://pharmatimes.com/news/",
        "https://www.worldpharmaceuticals.net/news/",
        "https://www.expresspharma.in/",
        "https://www.pmlive.com/",
        "https://firstwordpharma.com/",
        "https://www.reuters.com/business/healthcare-pharmaceuticals",
        "https://pharmanewsintel.com/"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/'
    }

    def start_requests(self):
        for link in self.start_urls:
            filename = urlparse(link).netloc + ".txt"
            try:
                textfile = open("/home/balaji/Desktop/webScraper/webScraper/htmlLinkFiles/" + filename, 'r')
                for url in textfile.readlines():
                    request = scrapy.Request(url=url, callback=self.parse, headers=self.headers)
                    yield request
            except:
                print('file not found')

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html5lib")
        textfile = open("/home/balaji/Desktop/webScraper/webScraper/htmlContentFiles/" + str(self.count) + ".txt", 'w')
        text = str(soup.find('body'))
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'[ \t]+', ' ', text.strip())
        textfile.write(text)
        self.count += 1
        textfile.close()
        print('content saved')
