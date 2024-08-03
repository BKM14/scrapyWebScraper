import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class XmlSpider(scrapy.Spider):
    name = "xmlScraper"
    start_urls = [
        "https://www.drugs.com/feeds/medical_news.xml",
        "https://www.drugs.com/feeds/headline_news.xml",
        "https://www.drugs.com/feeds/fda_alerts.xml",
        "https://www.drugs.com/feeds/new_drug_approvals.xml",
        "https://www.drugs.com/feeds/new_drug_applications.xml",
        "https://www.drugs.com/feeds/clinical_trials.xml",
        "https://www.fiercepharma.com/rss/xml",
        "https://www.pharma-iq.com/rss/categories/clinical",
        "https://www.pharmiweb.com/rss/press-releases-7-days",
        "https://www.pharmiweb.com/rss/articles",
        "https://www.pharmiweb.com/rss/pwtoday"
        "https://www.worldpharmanews.com/?format=feed&type=rss",
        "https://pharmatimes.com/news/feed/",
        "https://pharmatimes.com/feed/",
        "https://pmlive.com/feed/"
    ]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/'
    }

    def start_requests(self):
        for url in self.start_urls:
            request = scrapy.Request(url=url, callback=self.parse, headers=self.headers)
            yield request

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'lxml')
        filename = urlparse(response.url).netloc + ".txt"
        textfile = open("./webScraper/data/xmlContentFiles/" + filename, "a")
        textfile.write(str(soup) + "\n\n\n")
        textfile.write("--------------------\n")
        textfile.close()
