# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HealthgradesSpiderItem(scrapy.Item):

	name = scrapy.Field()
	gender = scrapy.Field()
	speciality = scrapy.Field()
	practice_name = scrapy.Field()
	completion_description = scrapy.Field()
	completion_year = scrapy.Field()
	edu_name = scrapy.Field()
	edu_type = scrapy.Field()
	street_address = scrapy.Field()
	city = scrapy.Field()
	state = scrapy.Field()
	zip_code = scrapy.Field()
	phone = scrapy.Field()
	responseCount = scrapy.Field()
	reviewCount = scrapy.Field()
	average_score = scrapy.Field()
	link = scrapy.Field() 

	raw_pes = scrapy.Field() 
	raw_view_model = scrapy.Field() 
