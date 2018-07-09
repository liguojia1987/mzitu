# encoding=utf-8

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import chardet

class MzituPipeline(object):
    def process_item(self, item, spider):   
        #print "process_item ==========================> "
        #print item['name']
        #print item['url']

        return item        

class MzituScrapyPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        #print "file_path ==============>"
        item = request.meta['item']
        #print item
        folder = item['name']
        folder_strip = strip(folder)
        #print chardet.detect(folder_strip)
        folder_strip = folder_strip.decode('utf-8','ignore')
        image_guid = request.url.split('/')[-1]
        #print "filename =========>"
        #filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        filename = "full/%s/%s" % (folder_strip, image_guid)
        #print filename
        #print "<================= filename"
        return filename

    def get_media_requests(self, item, info):
        #print "get_media_requests ===================>"
        for img_url in item['image_urls']:
            #print item
            referer = item['url']            
            yield Request(img_url, meta={'item': item,'referer': referer})


    def item_completed(self, results, item, info):
        #print "item_completed ===================>"
        #print results
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    # def process_item(self, item, spider):
    #     return item

def strip(path):
    #print "strip =================>"
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path
