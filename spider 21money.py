#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import json
import re

# 21经济网-经济

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
res_data = {}


def getData():
    for page in range(10, 1, -1):
        print(page)
        url = 'http://www.21jingji.com/channel/money/'+str(page)+'.html?r=1494321482'
        html = requests.get(url, headers=headers)
        Soup = BeautifulSoup(html.text, 'lxml')
        all_a = Soup.find_all('div',class_='Tlist')
        for a in all_a[::-1]:
            href =a.find('a', attrs={"href": re.compile(r'^http://www.21jingji.com/2017')})
            res_data['url']=href['href']



            url2 = res_data['url']
            html2 = requests.get(url2, headers=headers)
            Soup2 = BeautifulSoup(html2.text, 'lxml')
            spans = Soup2.find('p', class_='Wh').find_all('span')
            res_data['source'] = spans[2].get_text().strip().encode('iso-8859-1').decode('utf-8')
            if spans[2] is None:
                res_data['source'] = ['21经济网']
            res_data['time1'] = spans[0].get_text().strip().encode('iso-8859-1').decode('utf-8')
            res_data['time2'] = spans[1].get_text().strip().encode('iso-8859-1').decode('utf-8')


            abstract=Soup2.find('p', class_='abstract backg')
            res_data['sumary']=abstract.get_text().strip().encode('iso-8859-1').decode('utf-8')

            Title=Soup2.find('title')
            res_data['Title']=Title.get_text().strip().encode('iso-8859-1').decode('utf-8')
            res_data['tags']=[]
            sid1=re.sub(r'http\:\/\/www\.21jingji\.com/','',res_data['url'])
            sid2=re.sub(r'\.html','',sid1)
            sid3=re.sub(r'/.....','',sid2)
            res_data['sid']=re.sub(r'2017','',sid3)

            year = re.sub(r'年', '', res_data['time1'])
            month = re.sub(r'月', '', year)
            day = re.sub(r'日', '', month)
            hour = re.sub(r':', '', res_data['time2'])
            t1 = int(day + hour)

            t2 = int(time.strftime('%Y%m%d%H%M'))
            t3 = t2 - t1


            if (t3 <= 15):  # 时间差值小于某个范围即为更新的数据,爬取历史数据值较大，爬去增量数据值设为间隔时间数据
                print(res_data['sid'],res_data['url'],res_data['time1']+res_data['time2'],res_data['Title'],res_data['source'],res_data['sumary'])



    print(1)
    url = 'http://www.21jingji.com/channel/money/'
    html = requests.get(url, headers=headers)
    Soup = BeautifulSoup(html.text, 'lxml')
    all_a = Soup.find_all('div', class_='Tlist')
    for a in all_a[::-1]:
        href = a.find('a', attrs={"href": re.compile(r'^http://www.21jingji.com/2017')})
        res_data['url'] = href['href']

        url2 = res_data['url']
        html2 = requests.get(url2, headers=headers)
        Soup2 = BeautifulSoup(html2.text, 'lxml')
        spans = Soup2.find('p', class_='Wh').find_all('span')
        res_data['source'] = spans[2].get_text().strip().encode('iso-8859-1').decode('utf-8')
        if res_data['source'] is None:
            res_data['source']=['21经济网']
        res_data['time1'] = spans[0].get_text().strip().encode('iso-8859-1').decode('utf-8')
        res_data['time2'] = spans[1].get_text().strip().encode('iso-8859-1').decode('utf-8')


        abstract = Soup2.find('p', class_='abstract backg')
        res_data['sumary'] = abstract.get_text().strip().encode('iso-8859-1').decode('utf-8')

        Title = Soup2.find('title')
        res_data['Title'] = Title.get_text().strip().encode('iso-8859-1').decode('utf-8')

        res_data['tags'] = []
        sid1 = re.sub(r'http\:\/\/www\.21jingji\.com/', '', res_data['url'])
        sid2 = re.sub(r'\.html', '', sid1)
        sid3 = re.sub(r'/.....', '', sid2)
        res_data['sid'] = re.sub(r'2017', '', sid3)

        year = re.sub(r'年', '', res_data['time1'])
        month = re.sub(r'月', '', year)
        day = re.sub(r'日', '', month)
        hour = re.sub(r':', '', res_data['time2'])
        t1 = int(day + hour) #发布时间
        t2 = int(time.strftime('%Y%m%d%H%M'))#实时时间
        t3 = t2 - t1  #时间差值


        if (t3 <= 15):  # 时间差值小于某个范围即为更新的数据,爬取历史数据值较大，爬去增量数据值设为间隔时间数据

            print(res_data['sid'], res_data['url'], res_data['time1'] + res_data['time2'], res_data['Title'],res_data['source'], res_data['sumary'])



getData()
