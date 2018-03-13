# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecondHandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    from_url = scrapy.Field()
    house_info_url = scrapy.Field()
    house_info_title = scrapy.Field()
    house_info_area_desc = scrapy.Field()
    house_info_desc = scrapy.Field()
    house_info_released_time = scrapy.Field()
    house_info_last_trade_time = scrapy.Field()
    house_info_tags = scrapy.Field()
    house_info_community_name = scrapy.Field()
    house_info_position = scrapy.Field()
    wait_seen_att_time = scrapy.Field()
    house_info_rooms = scrapy.Field()
    house_num_area = scrapy.Field()
    house_char_floor = scrapy.Field()
    house_num_floor_total = scrapy.Field()
    house_char_toward = scrapy.Field()
    house_char_decoration = scrapy.Field()
    house_char_elevator_ratio = scrapy.Field()
    house_char_has_elevator = scrapy.Field()
    house_char_building_type = scrapy.Field()
    house_char_building_struc = scrapy.Field()
    house_char_trading_ownship = scrapy.Field()
    house_char_usage = scrapy.Field()
    house_char_property_ownship = scrapy.Field()
    house_char_own_years = scrapy.Field()
    house_pay_total = scrapy.Field()
    house_pay_unit = scrapy.Field()
    house_pay_per = scrapy.Field()
    house_pay_per_unit = scrapy.Field()
    house_pay_first = scrapy.Field()
    y_seen7 = scrapy.Field()
    y_seen30 = scrapy.Field()
    house_char_visit_time = scrapy.Field()
    house_district = scrapy.Field()
    house_site = scrapy.Field()
    community_name = scrapy.Field()
    community_url = scrapy.Field()
    community_mean_price = scrapy.Field()
    community_mean_price_urit = scrapy.Field()
    community_help_fee = scrapy.Field()
    community_building_num = scrapy.Field()
    community_house_num = scrapy.Field()

