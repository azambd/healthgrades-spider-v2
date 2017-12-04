# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import HealthgradesSpiderItem
import json
import re

#Header For Sleep Timer
from time import sleep
import random

sleep(random.randrange(4,6))

class HealthgradesSpider(CrawlSpider):
    name = 'healthgrades'
    allowed_domains = ['healthgrades.com']

    start_urls = ['http://healthgrades.com/']

    rules = (
        Rule(
            LinkExtractor(
                # allow= (r'physician/\S+',), #https://www.healthgrades.com/physician/dr-richard-pearce-2dmnh/comments?currentPage=2
                allow = (r'physician/.*-[0-9a-z]*',), #https://www.healthgrades.com/physician/dr-james-kennedy-263bh
                unique=True,
            ), 
            callback='parse_item', 
            follow=True
        ),
    )

    def parse_item(self, response):
        
        item = HealthgradesSpiderItem()

        item['name'] = response.xpath('//div[@class="provider-name"]/h1/text()').extract_first()
        # for names in item['name']:
        #     if names == '':
        #         continue
        #     else:
        #         item['name'] = response.xpath('//div[@class="provider-name"]/h1/text()').extract_first()

        item['link'] = response.url
        item['speciality'] = response.xpath('//div[@class="provider-speciality"]/span/text()').extract_first()
        item['gender'] = response.xpath('//div[@class="provider-gender"]/span/text()').extract_first()
        #item['street_address'] = response.xpath('//p[@itemprop="streetAddress"]/text()').extract_first()
        #item['city'] = response.xpath('//p[@class="city-state-info"]/span[@itemprop="addressLocality"]/text()').extract_first()
        #item['state'] = response.xpath('//p[@class="city-state-info"]/span[@itemprop="addressRegion"]/text()').extract_first()
        #item['zip_code'] = response.xpath('//p[@class="city-state-info"]/span[@itemprop="postalCode"]/text()').extract_first()
        #Parsing from inside JS for 2 fields: review_numbers and average_score
        pattern = r'pageState.pes \= {.*}'
        h = response.xpath('//*[@type="text/javascript"]')[6].re(pattern)
        i = [w.replace('pageState.pes', '') for w in h]
        i = [w.replace('=', '') for w in i]
        i = ''.join(i)
        d = json.loads(i) #This is JSON structure of the data
        item['responseCount'] = d['model']['overall']['responseCount']
        item['reviewCount'] = d['model']['overall']['reviewCount']
        item['average_score'] = d['model']['overall']['roundedScore']
        #Parsing Education information from JS data 
        edu_pattern = r'pageState.premiumProfile \= {.*}'
        edu_json_search = response.xpath('//*[@type="text/javascript"]')[6].re(edu_pattern)
        edu_json_data = [e.replace('pageState.premiumProfile', '') for e in edu_json_search]
        edu_json_data = [e.replace('=', '') for e in edu_json_data]
        edu_json_data = ''.join(edu_json_data)
        edu_json = json.loads(edu_json_data)
        item['practice_name'] = edu_json['officeLocations'][0]['practiceName']
        item['city'] = edu_json['officeLocations'][0]['city']
        item['state'] = edu_json['officeLocations'][0]['state']
        item['zip_code'] = edu_json['officeLocations'][0]['postalCode']
        item['phone'] = edu_json['officeLocations'][0]['phone']
        item['street_address'] = edu_json['officeLocations'][0]['street']
        item['completion_description'] = edu_json['education'][0]['completionDescription']
        item['completion_year'] = edu_json['education'][0]['completionYear']
        item['edu_name'] = edu_json['education'][0]['name']
        item['edu_type'] = edu_json['education'][0]['type']

        yield item
