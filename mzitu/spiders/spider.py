# encoding=utf-8

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mzitu.items import MzituItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Spider(CrawlSpider):
    name = 'mzitu'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/120410',), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')), callback='parse_item', follow=True),
    )
    page_name = ''
    page_url = ''
    image_urls = []


    def parse_item(self, response):
        #print "parse_item ============>"
        self.page_name = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        self.page_url = response.url

        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            self.image_urls.append(img_url) 
        
        # max_num为页面最后一张图片的位置
        max_num = response.xpath("descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(default="N/A")
        for num in range(2, int(max_num)+1):
            # page_url 为每张图片所在的页面地址
            page_url = response.url + '/' + str(num)
            #print page_url
            yield Request(page_url, callback=self.img_url)

    def img_url(self, response,):
        item = MzituItem()
        item['name'] = self.page_name
        item['url'] = self.page_url
        item['image_urls'] = self.image_urls

        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            item['image_urls'].append(img_url)
        yield item
