#!/bin/sh
echo ImmoScraper starting.


echo Perform scraping.
for spider in `find spiders -type f -name "*Spider.py" -exec basename {} .py ';';`; do
    echo Running $spider
    scrapy crawl $spider
done
echo Scraping done





echo ImmoScraper done.