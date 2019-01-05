#!/bin/sh
echo ####### ImmoScraper starting.


echo ####### Perform scraping.
for spider in `find spiders -type f -name "*Spider.py" -exec basename {} .py ';';`; do
    echo Running $spider
    scrapy crawl $spider
done
echo ####### Scraping done

echo ####### Sending mails
python reporter/Reporter.py $1 $2
echo ####### Sending mails done

echo ####### ImmoScraper done.
