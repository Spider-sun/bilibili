# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json

from bilibili.items import BilibiliItem


class BilibiliSpiderSpider(scrapy.Spider):
    name = 'bilibili_spider'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.bilibili.com/x/tag/info?tag_id=0']

    def start_requests(self):
        for i in range(1, 99999999):
            # yield Request('https://api.bilibili.com/x/tag/info?tag_id={tag_id}'.format(tag_id=i))
            yield Request('https://api.bilibili.com/x/space/acc/info?mid={tag_id}&jsonp=jsonp'.format(tag_id=i))

    def parse(self, response):
        data = json.loads(response.body.decode('utf-8'))
        _id = data['data']['mid']
        info = data['data']
        item = BilibiliItem(_id=_id, info=info)
        yield item



    # def parse(self, response):
    #     for i in range(1, 99999999):
    #         yield Request('https://api.bilibili.com/x/tag/info?tag_id={tag_id}'.format(tag_id=i), callback=self.get_infos)
    #
    # def get_infos(self, response):
    #     data = json.loads(response.body.decode('utf-8'))
    #     _id = data['data']['tag_id']
    #     info = data['data']
    #     item = BilibiliItem(_id=_id, info=info)
    #     yield item