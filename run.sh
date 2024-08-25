#!/bin/sh

rm -rf ./webScraper/data/

mkdir -p ./webScraper/data/htmlContentFiles
mkdir -p ./webScraper/data/htmlLinkFiles
mkdir -p ./webScraper/data/xmlContentFiles

scrapy crawl xmlScraper
scrapy crawl htmlScraper
scrapy crawl htmlLinks

cd ./webScraper/data || exit

echo Please go to http://localhost:8000 to see the data
echo Press Ctrl + c to stop the container

python -m http.server 8000