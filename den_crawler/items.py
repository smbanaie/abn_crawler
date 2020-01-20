# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AbnCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    abn = scrapy.Field()
    legal_name = scrapy.Field()
    entity_type = scrapy.Field()
    abn_status = scrapy.Field()
    gst= scrapy.Field()
    business_location = scrapy.Field()
    trading_names = scrapy.Field()
    business_names = scrapy.Field()
    

class BusinessItem(scrapy.Item):
    # define the fields for your item here like:
    abns = scrapy.Field()  
    business_name = scrapy.Field()  
    address = scrapy.Field()    
    principal_address = scrapy.Field()    
    holder_names = scrapy.Field()    
    status = scrapy.Field()    
    registration_date = scrapy.Field()    
    holder_types = scrapy.Field()   
    
      
    
