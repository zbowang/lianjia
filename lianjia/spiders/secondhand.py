# -*- coding: utf-8 -*-
import scrapy
from lianjia.settings import CITY2URL
import json
from lianjia.items import SecondHandItem

class SecondHandSpider(scrapy.Spider):

    name = "secondhand"

    def __init__(self, *args, **kwargs):
        scrapy.Spider.__init__(self, *args, **kwargs)
        self.baseurl = CITY2URL[self.city]
        self.community_info = {}
    
    def start_requests(self):
        url =  self.baseurl + '/ershoufang/'
        yield scrapy.Request(url=url, callback = self.parse_first, dont_filter = True)

    # def start_requests(self):
    #     url =  'https://sh.lianjia.com/ershoufang/pudong/a4p1/'
    #     yield scrapy.Request(url=url, callback = self.parse_room, dont_filter = True)
    
    

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
            yield from self.to_simple(response.url, totalpage)


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
            yield from self.to_simple(response.url, totalpage)

    def parse_price(self, response):
        '''对该价格下的页面进行解析，判断是否超过100页，判断是否要根据面积细分抓取'''
        totalpage, has100 = self.has_page_100(response)
        if has100:
            for i in range(1, 8):
                area_url = '{}a{}/'.format(response.url, i)
                yield scrapy.Request(url = area_url, callback = self.parse_area, dont_filter = True)
        else:
            yield from self.to_simple(response.url, totalpage)

    def parse_area(self, response):
        '''对该面积下的页面进行解析，判断是否超过100页，判断是否要根据房间数细分抓取'''
        totalpage, has100 = self.has_page_100(response)
        if has100:
            for i in range(1, 7):
                room_url = '{}l{}/'.format(response.url, i)
                yield scrapy.Request(url = room_url, callback = self.parse_room, dont_filter = True)
        else:
            yield from self.to_simple(response.url, totalpage)

    def parse_room(self, response):
        '''对该房间数下的页面进行解析，判断是否超过100页，不超过就正常抓取，超过就不要那些数据了'''
        totalpage, has100 = self.has_page_100(response)
        if not has100:
            yield from self.to_simple(response.url, totalpage)
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
        if totalpage is not None: # None说明没有找到page-data
            for i in range(1, totalpage + 1):
                urli = '{}pg{}/'.format(url, i)
                yield scrapy.Request(url = urli, callback = self.parse_simple, dont_filter = True)

    def parse_simple(self, response):
        '''解析一级页面，获取每个房子的url和详情页中没有的数据'''
        house_list = response.css('.sellListContent li')
        for house in house_list:
            item = SecondHandItem()
            item['from_url'] = response.url
            item['wait_seen_att_time'] = house.css('.followInfo::text').extract_first()

            detail_url = house.css('.title a::attr(href)').extract_first()
            yield scrapy.Request(url = detail_url, callback = self.parse_detail, 
                                 meta = {'item': item}, dont_filter = True)
            

    def parse_detail(self, response):
        '''解析详情页，并获取小区详情页面'''
        item = response.meta['item']
        item['house_info_url'] = response.url
        item['house_info_title'] = response.css('.title h1::attr(title)').extract_first()
        item['house_info_area_desc'] = ''.join(response.css('.layout #infoList div div::text').extract())
        house_info_desc = response.css('.introContent div div::text').extract()
        item['house_info_desc'] = ''.join(i.strip() for i in house_info_desc)
        item['house_info_released_time'] = response.xpath('//div[@class="transaction"]//ul/li[1]/span[2]/text()').extract_first()
        item['house_info_last_trade_time'] = response.xpath('//div[@class="transaction"]//ul/li[3]/span[2]/text()').extract_first()
        item['house_info_tags'] = ' '.join(response.css('.introContent .tags .content a::text').extract())
        item['house_info_position'] = response.css('script').re_first("resblockPosition:'(.*?)'")
        item['house_info_rooms'] = response.xpath('//div[@class="base"]//li[1]/text()').extract_first()
        item['house_num_area'] = response.xpath('//div[@class="base"]//li[3]/text()').extract_first()[:-1]
        item['house_char_floor'] = response.xpath('//div[@class="base"]//li[2]/text()').extract_first()[:3]
        item['house_num_floor_total'] = response.xpath('//div[@class="base"]//li[2]/text()').re_first('共(.*?)层')
        item['house_char_toward'] = response.xpath('//div[@class="base"]//li[7]/text()').extract_first()
        item['house_char_decoration'] = response.xpath('//div[@class="base"]//li[9]/text()').extract_first()
        item['house_char_elevator_ratio'] = response.xpath('//div[@class="base"]//li[10]/text()').extract_first()
        item['house_char_has_elevator'] = response.xpath('//div[@class="base"]//li[11]/text()').extract_first()
        item['house_char_building_type'] = response.xpath('//div[@class="base"]//li[6]/text()').extract_first()
        item['house_char_building_struc'] = response.xpath('//div[@class="base"]//li[8]/text()').extract_first()
        item['house_char_trading_ownship'] = response.xpath('//div[@class="transaction"]//ul/li[2]/span[2]/text()').extract_first()
        item['house_char_usage'] = response.xpath('//div[@class="transaction"]//ul/li[4]/span[2]/text()').extract_first()
        item['house_char_property_ownship'] = response.xpath('//div[@class="transaction"]//ul/li[6]/span[2]/text()').extract_first()
        item['house_char_own_years'] = response.xpath('//div[@class="transaction"]//ul/li[5]/span[2]/text()').extract_first()
        item['house_pay_total'] = response.css('.price .total::text').extract_first()
        item['house_pay_unit'] = response.css('.price .unit span::text').extract_first()
        item['house_pay_per'] = response.css('.unitPrice span::text').extract_first()
        item['house_pay_per_unit'] = response.css('.unitPrice span i::text').extract_first()
        item['house_pay_first'] = response.css('.taxtext span::text').extract_first()
        item['y_seen7'] = response.css('.panel .count::text').extract_first()
        item['y_seen30'] = response.css('.totalCount span::text').extract_first()
        item['house_char_visit_time'] = response.css('.visitTime .info::text').extract_first()
        item['house_district'] = response.css('.areaName .info a::text').extract_first()
        item['house_site'] = ' '.join(response.css('.areaName .info a::text').extract()[1:])
        community_name = response.css('.communityName a::text').extract_first()
        if community_name in self.community_info.keys():
            item['community_name'] = self.community_info[community_name]['community_name']
            item['community_url'] = self.community_info[community_name]['community_url']
            item['community_mean_price'] = self.community_info[community_name]['community_mean_price']
            item['community_mean_price_unit'] = self.community_info[community_name]['community_mean_price_unit']
            item['community_help_fee'] = self.community_info[community_name]['community_help_fee']
            item['community_building_num'] = self.community_info[community_name]['community_building_num']
            item['community_house_num'] = self.community_info[community_name]['community_house_num']
            yield item
        else:
            community_url = self.baseurl + response.css('.communityName a::attr(href)').extract_first()
            yield scrapy.Request(url = community_url, callback = self.parse_community, 
                                 meta = {'item': item}, dont_filter = True)

    def parse_community(self, response):
        '''解析小区页面'''
        item = response.meta['item']
        community_name = response.css('.detailTitle::text').extract_first()
        community_url = response.url
        community_mean_price = response.css('.xiaoquUnitPrice::text').extract_first()
        community_mean_price_unit = response.css('.xiaoquPrice .fl::text').extract_first()
        community_help_fee = response.xpath('//div[@class="xiaoquInfo"]/div[3]/span[2]/text()').extract_first()
        community_building_num = response.xpath('//div[@class="xiaoquInfo"]/div[6]/span[2]/text()').extract_first()[:-1]
        community_house_num = response.xpath('//div[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract_first()[:-1]

        mydict = {
        'community_name': community_name,
        'community_url': community_url,
        'community_mean_price': community_mean_price,
        'community_mean_price_unit': community_mean_price_unit,
        'community_help_fee': community_help_fee,
        'community_building_num': community_building_num,
        'community_house_num': community_house_num
        }
        self.community_info[community_name] = mydict

        item['community_name'] = community_name
        item['community_url'] = community_url
        item['community_mean_price'] = community_mean_price
        item['community_mean_price_unit'] = community_mean_price_unit
        item['community_help_fee'] = community_help_fee
        item['community_building_num'] = community_building_num
        item['community_house_num'] = community_house_num
        yield item







    	


