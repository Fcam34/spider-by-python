#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import json
import re

#第一财经

headers = {'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'www.yicai.com',
            'Referer':'http://www.yicai.com/news/',
            'Cookie':'yu_id=c69f768bc51f41afa8c08b38093a8741; CNZZDATA1256870507=434207651-1494311154-%7C1494829890; _ga=GA1.2.1457825582.1494315189; _gid=GA1.2.1704541083.1494834243; Hm_lvt_80b762a374ca9a39e4434713ecc02488=1494315189,1494464998,1494553577; Hm_lpvt_80b762a374ca9a39e4434713ecc02488=1494834244; cn_ff152588baaf1u0970f0_dplus=%7B%22distinct_id%22%3A%20%2215bec2042755e0-003b7fc739d77f-396b4e08-1fa400-15bec204276d33%22%2C%22initial_view_time%22%3A%20%221494311154%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201494834247%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201494834247%7D; UM_distinctid=15bec2042755e0-003b7fc739d77f-396b4e08-1fa400-15bec204276d33',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
}
res_data={}

def getData():
    print('第一财经')
    for page in range(5,0,-1):#2273
        print(page)
        url = 'http://www.yicai.com/api/ajax/NsList/'+str(page)+'/77'
        html = requests.get(url, headers=headers)
        Soup =BeautifulSoup(html.text, 'lxml').encode('iso-8859-1').decode('utf-8')

        res=re.compile(r'<p class="f-ff1 f-fs14">+.*[\u4e00-\u9fa5]+')
        ps=res.findall(Soup)
        for p in ps:
            res_data['digest']=re.sub(r'<p class="f-ff1 f-fs14">','',p)+'。'
            print(res_data['sumary'])



        rex1=re.compile(r'http://www.yicai.com/news/+[0-9]+.html')
        reqs=rex1.findall(Soup)
        for req in reqs[::-2]:
            res_data['url']=req
            sid=re.sub('http\:\/\/www\.yicai\.com\/news\/','',res_data['url'])
            res_data['sid']=re.sub('.html','',sid)

            url1=res_data['url']
            res_data['tags']=['']
            res_data['sumary']=''
            html1 = requests.get(url1, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'})
            Soup1 = BeautifulSoup(html1.text, 'lxml')
            titles=Soup1.find('h1',class_='f-ff1 f-fwn f-fs30')
            res_data['title']=titles.get_text().encode('iso-8859-1').decode('utf-8')
            info=Soup1.find('h2',class_='f-ff1 f-fwn f-fs14')
            sumary=info.find('i')
            if sumary is not None:
                res_data['fromType']=sumary.get_text().encode('iso-8859-1').decode('utf-8')
            else:
                res_data['fromType']='第一财经'
            kind=info.find('a')
            res_data['kind']=kind.get_text().encode('iso-8859-1').decode('utf-8')
            spans=info.find_all('span')
            for span1 in spans[::2]:
                if span1 is '<span></span>':
                    res_data['author']=''
                else:
                    res_data['author'] = span1.get_text().encode('iso-8859-1').decode('utf-8')
            for span2 in spans[1::2]:
                res_data['ptime']=span2.get_text().encode('iso-8859-1').decode('utf-8')
           print(res_data['sid'],res_data['fromType']+' '+res_data['kind']+' '+res_data['author'], res_data['ptime'], res_data['sumary'],res_data['title'], res_data['tags'], res_data['url'])

          


getData()
