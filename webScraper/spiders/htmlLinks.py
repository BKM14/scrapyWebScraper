import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


def clean_and_merge_text(text):
    segments = re.split(r'(\.)', text)
    cleaned_segments = []

    current_segment = ""

    for segment in segments:
        segment = re.sub(r'\n+', '\n', segment)
        segment = re.sub(r'[ \t]+', ' ', segment)

        current_segment += segment

        if segment == '.':
            if current_segment.strip():
                cleaned_segments.append(current_segment.strip())
                current_segment = ""

    cleaned_text = '. '.join(cleaned_segments)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', cleaned_text)

    if not cleaned_text.endswith('.'):
        cleaned_text += '.'

    return cleaned_text


class LinksSpider(scrapy.Spider):
    name = "htmlLinks"
    count = 0
    start_urls = [
        "https://www.fiercepharma.com/",
        "https://www.worldpharmanews.com/",
        "https://pharmatimes.com/news/",
        "https://www.worldpharmaceuticals.net/news/",
        "https://health.economictimes.indiatimes.com/news/pharma",
        "https://pmlive.com/",
        "https://firstwordpharma.com/",
        "https://www.techtarget.com/pharmalifesciences"
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
                textfile = open("./webScraper/data/htmlLinkFiles/" + filename, 'r')
                for url in textfile.readlines():
                    request = scrapy.Request(url=url, callback=self.parse, headers=self.headers)
                    yield request
            except Exception as e:
                print('file not found')
                print(e)

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.text, "html5lib")
        textfile = open("./webScraper/data/htmlContentFiles/" + str(self.count) + ".txt", 'w')
        text = soup.find('body')
        for tag in ['script', 'path', 'style', 'a']:
            for tagElements in text.find_all(tag):
                tagElements.decompose()

        textfile.write(clean_and_merge_text(text.get_text()))
        self.count += 1
        textfile.close()
        print('content saved')
