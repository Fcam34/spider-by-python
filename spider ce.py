#-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import json
import re


#中国经济网 - 股市滚动新闻

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
res_data = {}
def getData():
    for page in range(4,0,-1):
        print(page+1) #显示页码
        url='http://finance.ce.cn/stock/gsgdbd/index_'+str(page)+'.shtml'#除了第一页外的url
        html = requests.get(url, headers=headers)
        Soup = BeautifulSoup(html.text, 'lxml')
        all_a = Soup.find_all('a', attrs={"href": re.compile(r'../../rolling/2017')})
        for a in all_a[::-1]:
            res_data['url'] =re.sub(r'\.\./\.\./','http://finance.ce.cn/',a['href'])
            res_data['Title']=a.get_text().strip().encode('iso-8859-1').decode('gbk')#来自中文编码的恶意
            
            url2=res_data['url']
            html2 = requests.get(url2, headers=headers)
            Soup2 = BeautifulSoup(html2.text, 'lxml')
            spans=Soup2.find('div',class_='laiyuan').find_all('span')
            res_data['source'] = spans[1].get_text().strip().encode('iso-8859-1').decode('gbk')
            res_data['fromType']=re.sub(r'来源：','',res_data['source']).strip() #除去‘来源：’方便显示
            res_data['time'] = spans[0].get_text().strip().encode('iso-8859-1').decode('gbk')

            sid=re.sub(r'\.\./\.\./rolling','',a['href'])
            sid2=re.sub(r'\.shtml','',sid)
            sid3=re.sub(r'/.........','',sid2)
            res_data['sid']=re.sub(r'_','',sid3)

            res_data['sumary'] = []#没有简介就显示为空数组
            res_data['tags'] = []#没有标签就显示为空数组
            data1 = [[res_data['sid'], res_data['fromType'], res_data['time'], res_data['sumary'], res_data['Title'],
                      res_data['tags'], res_data['url']]]
            names = 'sid fromType pubTime sumary title tags url'.split()
            for d in data1:
                data2 = dict(zip(names, d))

                with open('pythonapp_ce.json', 'a', encoding='utf-8') as writer1:
                    json_data = json.dumps(data2, sort_keys=False, indent=2, separators=(',', ': '), ensure_ascii=False)
                    print(json_data, file=writer1)


            print(res_data['sid'],res_data['Title'],res_data['time'],res_data['fromType'],res_data['url'])



#首页的相关信息

    print(1)
    url1 = 'http://finance.ce.cn/stock/gsgdbd/index.shtml'#第一页URL
    html1 = requests.get(url1, headers=headers)
    Soup1 = BeautifulSoup(html1.text, 'lxml')
    all_a = Soup1.find_all('a', attrs={"href": re.compile(r'../../rolling/2017')})
    for a in all_a[::-1]:
        res_data['url'] = re.sub(r'\.\./\.\./', 'http://finance.ce.cn/', a['href'])
        res_data['Title'] = a.get_text().strip().encode('iso-8859-1').decode('gbk')

        url3 = res_data['url']
        html3 = requests.get(url3, headers=headers)
        Soup3 = BeautifulSoup(html3.text, 'lxml')
        spans = Soup3.find('div', class_='laiyuan').find_all('span')
        res_data['source'] = spans[1].get_text().strip().encode('iso-8859-1').decode('gbk')
        res_data['fromType'] = re.sub(r'来源：', '', res_data['source']).strip()
        res_data['time'] = spans[0].get_text().strip().encode('iso-8859-1').decode('gbk')
        sid4 = re.sub(r'\.\./\.\./rolling', '', a['href'])
        sid5 = re.sub(r'\.shtml', '', sid4)
        sid6 = re.sub(r'/.........', '', sid5)
        res_data['sid'] = re.sub(r'_', '', sid6)
        res_data['sumary'] = []
        res_data['tags'] = []

        data3 = [[res_data['sid'], res_data['fromType'], res_data['time'], res_data['sumary'], res_data['Title'], res_data['tags'], res_data['url']]]
        names1 = 'sid fromType pubTime sumary title tags url'.split()
        for d in data3:
            data4 = dict(zip(names1, d))
           
            with open('pythonapp_ce.json', 'a', encoding='utf-8') as writer1:
                json_data = json.dumps(data2, sort_keys=False, indent=2, separators=(',', ': '), ensure_ascii=False)
                print(json_data, file=writer1)

        print(res_data['sid'],res_data['Title'], res_data['time'], res_data['fromType'],res_data['url'])

getData()
