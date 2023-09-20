import scrapy
from testscraper.items import TestscraperItem
from urllib.parse import urljoin
import json
from datetime import datetime, timedelta
import pandas as pd
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb3J1bV9rZXkiOiJuZXdzIiwiZ3JhbnRfdHlwZSI6ImFsZXhfY3JlZGVudGlhbHMiLCJzY29wZSI6W10sImV4cCI6MTY5NDc5NTg4MiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9DTElFTlQiXSwianRpIjoiMDFlNWViM2MtMzc3YS00Y2RmLTllY2ItZGE4YzE1ZWExYjIyIiwiZm9ydW1faWQiOi05OSwiY2xpZW50X2lkIjoiMjZCWEF2S255NVdGNVowOWxyNWs3N1k4In0.umRqXPe_xfDU1vJ-peB5cdDvXCrAYfKsgY4faqefXtA'
    }

class DaumSpider(scrapy.Spider):

    name = "daumnews"
    topics = ['health', 'life', 'art', 'book', 'leisure', 'others', 'weather', 'fashion', 'home', 'food','religion']
    base_url = 'https://news.daum.net/breakingnews/culture/{}?page={}&regDate={}'

    # 크롤링 날짜 지정
    start_date = datetime(2023, 9, 16)
    end_date = datetime(2023, 9, 18)

    def start_requests(self):
        for topic in self.topics:
            # self.detail_topic = topic
            current_date = self.start_date
            while current_date <= self.end_date:
                date = current_date.strftime('%Y%m%d')
                url = self.base_url.format(topic, 1, date)
                yield scrapy.Request(url=url, callback=self.parse, headers=headers,
                                      meta={'page': 1, 'topic': topic, 'current_date': date})
                current_date += timedelta(days=1)

    def parse(self, response):
        # 기사 링크
        article_url = response.xpath('//*[@id="mArticle"]/div[3]/ul/li/div/strong/a/@href').extract()
        for url in article_url:
            # self.detail_url = url
            yield scrapy.Request(url=url, callback=self.parse_detail, headers=headers, 
                                 meta={'detail_topic': response.meta['topic'], 'detail_url': url})
            
        # # 다음 페이지로 이동
        # while True:
        #     next_page = response.meta['page'] + 1
        #     next_url = self.base_url.format(response.meta['topic'], next_page, response.meta['current_date'])
        #     if response.xpath('//*[@id="mArticle"]/div[3]/text()').extract != '다':
        #         yield scrapy.Request(url=next_url, callback=self.parse, headers=headers, 
        #                              meta={'page': next_page, 'topic': response.meta['topic'], 'current_date': response.meta['current_date']})
        #     else:
        #         break
            
    # 날짜, 기자, 제목, 본문 크롤링
    def parse_detail(self, response):
        date = response.xpath('//*[@id="mArticle"]/div[1]/div[1]/span[2]/span/text()').extract()
        writer = response.css('#mArticle > div.head_view > div.info_view > span:nth-child(1)::text').extract()
        title = response.css('.tit_view::text').extract()
        content = response.xpath('//*[@id="mArticle"]/div[2]/div[2]/section/p/text()').extract()

        item = TestscraperItem()
        item['platform_id'] = 'Daum'
        item['cat1_id'] = 'Culture'
        item['cat2_id'] = response.meta['detail_topic']
        item['date'] = date
        item['writer'] = writer
        item['title'] = title
        item['content'] = content
        item['url'] = response.meta['detail_url']

        yield item

        # 각 뉴스기사별 감정 스티커 json url 추출
    #     sticker_key = re.search(r'(\d+)', response.meta['detail_url']).group(1)
    #     sticker_base_url = "https://action.daum.net/apis/v1/reactions/"
    #     endpoint = f"home?itemKey={sticker_key}"
    #     sticker_url = urljoin(sticker_base_url, endpoint)
    #     yield scrapy.Request(url=sticker_url, callback=self.emotion_sticker, headers=headers, meta={'item': item})

    # def emotion_sticker(self, response):
    #     data = json.loads(response.text)
    #     item = response.meta['item']
    #     stickers = {
    #         'Recommend': data["item"]["stats"].get("RECOMMEND", 0),
    #         'Like': data["item"]["stats"].get("LIKE", 0),
    #         'Impress': data["item"]["stats"].get("IMPRESS", 0),
    #         'Angry': data["item"]["stats"].get("ANGRY", 0),
    #         'Sad': data["item"]["stats"].get("SAD", 0)
    #     }
    #     item['sticker'] = stickers
    #     yield item