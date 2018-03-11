# -*- coding: utf-8 -*-
import scrapy
from lianjia.settings import CITY2URL
import json



class SecondHandSpider(scrapy.Spider):

    name = "secondhand"

    def __init__(self, urlname=None, *args, **kwargs):
        scrapy.Spider.__init__(self, *args, **kwargs)
        self.baseurl = CITY2URL[self.city]
    
    def start_requests(self):
        url =  self.baseurl + '/ershoufang/'
        yield scrapy.Request(url=url, callback = self.parse_first, dont_filter = True)
    

    def parse_first(self, response):
        '''对一个城市二手房首页进行解析，判断是要是否要细分成区抓取'''
        totalpage, has100 = self.has_page_100(response)

        if has100:
            xpath_str = '//div[@class="position"]/dl[2]/dd/div[@data-role="ershoufang"]//a/@href'
            district_half_url_list = response.xpath(xpath_str).extract()
            for district_half_url in district_half_url_list:
                district_url = self.baseurl + district_half_url
                yield scrapy.Request(url = district_url, callback = self.parse_district, dont_filter = True)
        else:
            self.to_simple(response.url, totalpage)

    # 从parse_dictrict到to_simple都是为了抓全所有房子进行的细分
    # parse_simple和parse_detail才是抓取的信息的主要代码

    def parse_district(self, response):
        '''对一个区进行解析，判断这个区是否超过100页，判断是否要根据价格细分抓取'''
        totalpage, has100 = self.has_page_100(response)
        if has100:
            for i in range(1, 8):
                price_url = '{}p{}/'.format(response.url, i)
                yield scrapy.Request(url = price_url, callback = self.parse_price, dont_filter = True)
        else:
            self.to_simple(response.url, totalpage)

    def parse_price(self, response):
        '''对该价格下的页面进行解析，判断是否超过100页，判断是否要根据面积细分抓取'''
        totalpage, has100 = self.has_page_100(response)
        if has100:
            for i in range(1, 8):
                area_url = '{}a{}/'.format(response.url, i)
                yield scrapy.Request(url = area_url, callback = self.parse_area, dont_filter = True)
        else:
            self.to_simple(response.url, totalpage)

    def parse_area(self, response):
        '''对该面积下的页面进行解析，判断是否超过100页，判断是否要根据房间数细分抓取'''
        totalpage, has100 = self.has_page_100(response)
        if has100:
            for i in range(1, 7):
                room_url = '{}l{}/'.format(response.url, i)
                yield scrapy.Request(url = room_url, callback = self.parse_room, dont_filter = True)
        else:
            self.to_simple(response.url, totalpage)

    def parse_room(self, response):
        '''对该房间数下的页面进行解析，判断是否超过100页，不超过就正常抓取，超过就不要那些数据了'''
        totalpage, has100 = self.has_page_100(response)
        if not has100:
            self.to_simple(response.url, totalpage)
        else:
            print('drop here')


    def has_page_100(self, response):
        '''看一个页面是否有100页，如果有说明这个页面需要被拆分'''
        dict_str = response.xpath('//div[@class="page-box fr"]/div/@page-data').extract_first()
        if dict_str:
            page_dict = json.loads(dict_str)
            totalpage = page_dict.get("totalPage")
            return totalpage, totalpage == 100
        print('page data not found in {}'.format(response.url))
        return None, None

    def to_simple(self, url, totalpage):
        '''对于没有100页的页面，构造每一页的url，传到`parse_simple`函数中解析'''
        # for i in range(1, totalpage + 1):
        #     urli = url + '/pg' + str(i)
        #     yield scrapy.Request(url = urli, callback = self.pase_simple, dont_filter = True)
        if totalpage is not None: # None说明没有找到page-data
            for i in [1, 2, totalpage]:
                urli = '{}pg{}/'.format(url, i)
                # yield scrapy.Request(url = urli, callback = self.pase_simple, dont_filter = True)
                print(urli)
            print('\n')

    def parse_simple(self, response):
        pass

    def parse_detail(self, response):
        pass




    	


