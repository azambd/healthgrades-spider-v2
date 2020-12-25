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
    start_urls = ['https://www.healthgrades.com/group-directory/ca-california/san-francisco',
            'https://www.healthgrades.com/internal-medicine-directory/ca-california/san-francisco']
    base_url = 'https://www.healthgrades.com/'


    rules = (
        # Crawl the site, but ignore non-directory links
        Rule(LinkExtractor(deny=[
            r'\/right-care\/.*',
            r'\/video\/.*',
            r'\/contributors\/.*',
            r'\/drugs\/.*',
            r'\/conditions\/.*',
            r'\/healthguides\/.*',
        ], unique=True), follow=True),

        # Physican links
        Rule(
            LinkExtractor(
                # allow= (r'physician/\S+',), #https://www.healthgrades.com/physician/dr-richard-pearce-2dmnh/comments?currentPage=2
                allow = (r'\/physician/.*-[0-9a-z]*',), #https://www.healthgrades.com/physician/dr-james-kennedy-263bh
                unique=True,
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        item = HealthgradesSpiderItem()

        item['link'] = response.url

        ## TODO remove hardcoded offset, should be searching for re in each item
        script_el = response.xpath('//*[@type="text/javascript"]')[4]

        # Parsing from inside JS for 2 fields: review_numbers and average_score
        pattern = r'pageState.pes \= {.*}'
        h = script_el.re(pattern)

        ## TODO this should be replaced with re groups 
        # ex. m = re.search(r'x = (.*?)') m.group(1)
        i = [w.replace('pageState.pes', '') for w in h]
        i = [w.replace('=', '') for w in i]
        i = ''.join(i)

        d = json.loads(i) #This is JSON structure of the data
        item['responseCount'] = d['model']['overall']['responseCount']
        item['reviewCount'] = d['model']['overall']['reviewCount']
        item['average_score'] = d['model']['overall']['roundedScore']

        # TODO Rename this to view_model
        # Parsing Education information from JS data
        edu_pattern = r'pageState.viewModel \= {.*}'
        edu_json_search = script_el.re(edu_pattern)
        edu_json_data = [e.replace('pageState.viewModel', '') for e in edu_json_search]
        edu_json_data = [e.replace('=', '') for e in edu_json_data]
        edu_json_data = ''.join(edu_json_data)

        edu_json = json.loads(edu_json_data)
        item['practice_name'] = edu_json['primaryOffice']['practiceName']
        item['city'] = edu_json['primaryOffice']['city']
        item['state'] = edu_json['primaryOffice']['state']
        item['zip_code'] = edu_json['primaryOffice']['postalCode']
        item['phone'] = edu_json['primaryOffice']['officePhone']
        item['street_address'] = edu_json['primaryOffice']['street']

        if len(edu_json['education']) > 0:
            primary_education = edu_json['education'][0] 
            item['completion_description'] = primary_education['completionDescription']
            item['completion_year'] = primary_education['completionYear']
            item['edu_name'] = primary_education['name']
            item['edu_type'] = primary_education['type']

        item['name'] = edu_json['providerDisplayFullName']
        item['speciality'] = edu_json['practicingSpecialityName']
        item['gender'] = edu_json['genderString']

        item['raw_pes'] = i
        item['raw_view_model'] = edu_json_data
        yield item
