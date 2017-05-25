from pyspider.libs.base_handler import *
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=10)
    def on_start(self):
        n = 1
        while(n<2715):          
            self.crawl('http://m.nbd.com.cn/columns/3/page/'+str(n), callback=self.index_page)
            n = n + 1

    @config(age=10 * 60)
    def index_page(self, response):
       
        for each in response.doc('a[href^="http"]').items():
            if 'http://m.nbd.com.cn/articles' in each.attr.href:
                self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2,age=10*24*60*60)
    def detail_page(self, response):
        timeAfrom = response.doc('small').text().split('\n')
        print len(timeAfrom)
        if len(timeAfrom) > 1:
            timep = timeAfrom[0]
            fromsource = timeAfrom[1]
        else: 
            timep = timeAfrom
            fromsource = ""
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "time":timep,
            "from":fromsource,
            "author":"",
            "content":response.doc('.n_articleContainer').html(),
            "pickingTime":time.time()
        }
