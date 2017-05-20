#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-05-16 18:45:38
# Project: passage

from pyspider.libs.base_handler import *
import random

class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url =  'http://www.cailianpress.com/v2/article/get_recommend_article'
        self.get_article_url =  'http://www.cailianpress.com/v2/article/h5_get_article'
        self.page_num = 1
        self.total_num = 30
    
    @every(minutes=0.5)
    def on_start(self):
        print "hahah"
        self.crawl(self.base_url+"?"+str(random.random()), callback=self.index_page)
       
        
    @config(age=1)
    def index_page(self, response):
        print response.json['data']
        for x in response.json['data']:
            print x
            self.crawl('http://www.example.com?id='+x['sort_score'],callback = self.detail_page,save = x)
   
        staid = x['sort_score'] 
        print x
        self.crawl(self.get_article_url+"?"+str(random.randint(0,99)), callback=self.index_page,method='POST', data={'type': -1, 'count':15, 'staid':staid})

    @config(priority=2)
    def detail_page(self, response):
        x = response.save
        return {
            "sort_score": x['sort_score'],
            "content": x['content'],
            "author": x['author'],
            "title":x['title'],
            "time":x['time'],
            "author":x['author']
        }  
        
