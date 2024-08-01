import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class CuisinesSpider(scrapy.Spider):
    name = "htmlScraper"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/'
    }

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

    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            yield request

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html5lib")
        data = soup.find_all('a')
        # File to save resources
        filename = urlparse(response.url).netloc + ".txt"
        textfile = open("./webScraper/htmlLinkFiles/" + filename, 'w')
        for tag in data:
            textfile.write(response.urljoin(str(tag['href'])) + "\n")
        textfile.close()
        print("saved")

