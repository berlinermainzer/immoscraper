#!/bin/sh
echo ImmoScraper starting.

for spider in `find spiders -type f -name "*Spider.py" -exec basename {} .py ';';`; do
    echo Running $spider
    scrapy crawl $spider
done




echo ImmoScraper done.