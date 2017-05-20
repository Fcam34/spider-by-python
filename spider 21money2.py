#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-05-16 18:45:38
# Project: passage

from pyspider.libs.base_handler import *
import random
import time

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url =  'http://www.21jingji.com/channel/money/' 
        self.page_num = 1
    
    @every(minutes=10)
    def on_start(self): 
        self.crawl(self.base_url+"?"+str(random.random()), callback=self.index_page)
              
        while(self.page_num < 11):
            self.page_num = self.page_num + 1
            url = 'http://www.21jingji.com/channel/money/'+str(self.page_num)+'.html?r='+str(int(time.time()))
            self.crawl(url, callback=self.index_page)
                
        
    def index_page(self, response): 
        for x in response.doc('a.listTit').items(): 
            self.crawl(x.attr.href, callback=self.detail_page)
         
              

    @config(age=60*60,priority=2)
    def detail_page(self, response): 
        return {
            "url": response.url,
            "title": response.doc('.titl').text(),
            "time":response.doc('.Wh > span').eq(0).text()+" "+ response.doc('.Wh > span').eq(1).text(),
            "from":response.doc('.baodao').text(),
            "author":response.doc('.Wh1').text(),
            "content":response.doc('.detailCont').html(),
            "pickingTime":time.time()
        }  
        
