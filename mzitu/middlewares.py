# encoding=utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class MeiZiTu(object):

    def process_request(self, request, spider):
    	#print "process_request =============>"
        referer = request.meta.get('referer', None)
        if referer:
            request.headers['referer'] = referer