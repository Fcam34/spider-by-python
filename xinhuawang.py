from pyspider.libs.base_handler import *
import re
import json
import time

class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.base_url =  'http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=1&cnt=16&tp=1&orderby=1' 
        self.node_id = '11147664'
        self.page_num = 1
        self.total_num = 100

    @every(minutes=10)
    def on_start(self):
         self.crawl(self.base_url, callback=self.index_page)

    @config(age=60 * 60)
    def index_page(self, response):
        result =  self.jsmToPym(response.text)
        print result
        self.total_num = result['totalnum']

            #从列表返回值中获取详情页地址
        for each in result['data']['list']:
            self.crawl(each['LinkUrl'], callback=self.detail_page,save = each)
         #把列表最后一个nodeid取出
        self.node_id = each['NodeId']  
        
        #判断获取到的数量是否超过总数，如果没有超过，则继续获取列表
        if self.page_num * 16 < self.total_num :
            self.page_num = self.page_num +1
            self.crawl('http://qc.wa.news.cn/nodeart/list?nid='+self.node_id+'&pgnum='+str(self.page_num)+'&cnt=16&tp=1&orderby=1', callback=self.index_page)
      
            
    @config(priority=2)
    def detail_page(self, response):
        x =  response.save
        return {
            "url": response.url,
            "title": x['Title'],
            "time":x['PubTime'],
            "from":x['SourceName'],
            "author":x['SourceName'],
            "content":response.doc('#p-detail').html(),
            "pickingTime":time.time(),
            "keyword":x['keyword']
        }  

    def jsmToPym(self,text):  
        a = text.replace('({','{').replace('})','}') 
        return  json.loads(a)
    
