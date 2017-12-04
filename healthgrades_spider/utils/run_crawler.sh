#!/bin/bash
PATH=$PATH:/usr/local/bin
export PATH
# source /home/ubuntu/projects/scrapingenv/bin/activate
#source /home/scraper/virtaulenvs/py2env/bin/activate
cd /home/engrfazam/healthgrades_spider/
scrapy crawl healthgrades
#deactivate
