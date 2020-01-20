# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from den_crawler.items import AbnCrawlerItem , BusinessItem
from scrapy.http import Request 
import codecs


class DenSpider(CrawlSpider):
    name = 'den'
    file_name = 'BUSINESS_NAMES_202001.csv'
    allowed_domains = ['abr.business.gov.au', 'connectonline.asic.gov.au']
    start_urls = []

    def start_requests(self):
        f = open(self.file_name,'r')
        next(f)
        for line in f : 
            abn = line.split('\t')[-1]
            if (len(abn)>0) : 
                url = f'https://abr.business.gov.au/ABN/View?id={abn}'
                yield Request(url=url, callback=self.parse_abn, dont_filter=True)
            
    def parse_business_name(self, response):
        try :
            
            # self.logger.info(f"\n parse_news called\n{response.request.url}\n")
            item = BusinessItem()
            item['abns'] = "^".join([k.replace(' ','') for k in "".join(response.xpath("//a[starts-with(@href, 'http://abr.business.gov.au/Search.aspx')]//text()").getall()).split(" (External Link)")[:-1]])
            item['business_name'] = response.xpath('//tr[th="Business name: "]/td/text()').get()
            if item['business_name'] : item['business_name']=item['business_name'].strip().replace(u'\xa0',' ')
            item['address'] = response.xpath('//tr[th="Address for service of documents: "]/td/text()').get()
            if item['address'] : item['address'] =item['address'].strip().replace(u'\xa0',' ')
            item['principal_address'] = response.xpath('//tr[th="Principal place of business: "]/td/text()').get()
            if item['principal_address'] : item['principal_address']=item['principal_address'].strip().replace(u'\xa0',' ')
            item['status'] = response.xpath('//tr[th="Status: "]/td/text()').get()
            if item['status'] : item['status']=item['status'].strip().replace(u'\xa0',' ')
            item['registration_date'] = response.xpath('//tr[th="Registration date: "]/td/text()').get()
            if item['registration_date'] : item['registration_date'] = item['registration_date'].strip().replace(u'\xa0',' ')
            item['holder_names'] = "^".join(response.xpath('//tr[th="Holder(s) details: "]/td/a/text()').getall())
            item['holder_types'] = "^".join(response.xpath('//tr[th="Holder(s) details: "]/td/text()').getall())
            if item['abns'] : 
                self.write_business_info(item)
            
        except Exception as err :
            print('*'*40)
            print(err)
            print('*'*40)
            
        
        

            
    def parse_abn(self, response):
        try :
            
            item = AbnCrawlerItem()
            item['gst'] = response.xpath('//tr[th="Goods & Services Tax (GST):"]/td/text()').get()
            if item['gst'] : item['gst'] =item['gst'].strip().replace(u'\xa0',' ')
            item['trading_names'] = "^".join([(k.strip().replace(u'\xa0',' ') if k else "") for k in response.xpath('//table[.//tr[th="Trading name"]]/tr/td/text()').getall()[2:] if len(k.strip().replace(u'\xa0',' ') ) >0])
            item['business_names'] = "^".join([(k.strip().replace(u'\xa0',' ') if k else "") for k in response.xpath('//table[.//tr[th="Business name"]]/tr/td//text()').getall()[1:] if len(k.strip().replace(u'\xa0',' ') ) >0 ])
            item['abn_status'] = response.xpath('//tr[th="ABN status:"]/td/text()').get()
            if item['abn_status'] : item['abn_status'] = item['abn_status'].strip().replace(u'\xa0',' ')
            item['abn'] = response.url[response.url.find('?id=')+4:]
            item['entity_type'] = response.xpath('//tr[th="Entity type:"]/td/a/text()').get()
            item['legal_name'] = response.xpath('//span[@itemprop="legalName"]/text()').get()
            item['business_location'] = response.xpath('//span[@itemprop="addressLocality"]/text()').get()
            business_urls = response.xpath("//a[starts-with(@href, 'https://connectonline.asic.gov.au/RegistrySearch')]/@href").getall()
            for url in business_urls:
                yield Request(url=url, callback=self.parse_business_name)
            if item['abn'] : 
                self.write_abn_info(item)
            
        except Exception as err :
            print('-'*40)
            print(err)
            print('-'*40)
            
        
    def write_abn_info(self, item):
        f = codecs.open('abn_info.csv', "a", encoding="utf8")
        row_csv = "{0}^^{1}^^{2}^^{3}^^{4}^^{5}^^{6}^^{7}\r\n".format(item["abn"],
                                                    item["legal_name"],
                                                    item["entity_type"],
                                                    item["abn_status"],
                                                    item["gst"],
                                                    item["business_location"],
                                                    item["business_names"],
                                                    item["trading_names"])
        f.write(row_csv)
        f.close()
        
    def write_business_info(self, item):
        f = codecs.open('abn_business_info.csv', "a", encoding="utf8")
        row_csv = "{0}^^{1}^^{2}^^{3}^^{4}^^{5}^^{6}^^{7}\r\n".format(
                                                    item["business_name"],
                                                    item["address"],
                                                    item["principal_address"],
                                                    item["status"],
                                                    item["registration_date"],
                                                    item["holder_names"],
                                                    item["holder_types"],
                                                    item["abns"])
        f.write(row_csv)
        f.close()
        