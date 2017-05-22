from pyspider.libs.base_handler import *
import re
import json
import time

class Handler(BaseHandler):
    headers= {
    'Host': 'm.yicai.com',
    'Connection': 'keep-alive',
    'Cache-Control':' max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Mobile Safari/537.36',
     'Accept':' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'DNT':' 1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Referer':'http://m.yicai.com/news/'
     }
    
    crawl_config = {
        "headers" : headers,
        "cookies" :{'yu_id':'3ee7dd842b984764ba0370c99abf18dd',
'CNZZDATA1256870507':'463320579-1495083697-%7C1495083697', 
'Hm_lvt_80b762a374ca9a39e4434713ecc02488':'1495010971,1495087126', 
'Hm_lpvt_80b762a374ca9a39e4434713ecc02488':'1495087892',
' _ga':'GA1.2.243360405.1495010971', 
' _gid':'GA1.2.144658919.1495087892', 
' cn_ff152588baaf1u0970f0_dplus':'%7B%22distinct_id%22%3A%20%2215c15990cc72b4-0db0aa7eec5898-143a655c-1fa400-15c15990cc843a%22%2C%22initial_view_time%22%3A%20%221495008097%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201495087891%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201495087891%7D; UM_distinctid=15c15990cc72b4-0db0aa7eec5898-143a655c-1fa400-15c15990cc843a'}
                   
    }
    
    def __init__(self):
        self.page_num = 1 

    @every(minutes=10)
    def on_start(self):
        self.crawl('http://m.yicai.com/news/',fetch_type='js', callback=self.get_more_list)
    
    def get_more_list(self,response):
        url = 'http://m.yicai.com/ajax/oneList/77/10/1' 
        self.crawl(url,callback=self.index_page)
        
        
    
    @config(age= 60 * 60)
    def index_page(self, response):
        text =  response.text
        quote_keys_regex = r'([\{\s,])(\w+)(:)'
        a = re.sub(quote_keys_regex, r'\1"\2"\3', text).replace('\'',"\"").replace('},]',"}]")
        result =  json.loads(a)
        print result['list']
        for item in result['list']:
            url = item['url']
            self.crawl(url,callback=self.detail_page)
        
        if result['anyMore'] == 'yes' :
            page_num = response.save['page_num'] if response.save else 1
            next_page = page_num+1
            url2 = 'http://m.yicai.com/ajax/oneList/77/10/'+str(next_page) 
            self.crawl(url2,callback=self.index_page,save={"page_num":next_page})
           
        

    @config(priority=2)
    def detail_page(self, response):
         return {
            "url": response.url,
            "title": response.doc('.m-txt-mb > .f-ff1').text(),
            "time":response.doc('h2 > span').eq(1).text(),
            "from":response.doc('i').text(),
            "author":response.doc('h2 > span').eq(0).text(),
            "content":response.doc('.m-text').html(),
            "pickingTime":time.time()
        }
 
        
        
        
        
        
        
        
        
        
        
