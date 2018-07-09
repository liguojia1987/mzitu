# encoding=utf-8

import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class MzituItem(scrapy.Item):
    name = scrapy.Field()
    image_urls = scrapy.Field()
    url = scrapy.Field()
    pass
