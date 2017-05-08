# coding=utf-8

from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import json
import re


#每经网 - 要闻

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
res_data = {}
def getData():
    for page in range(541,0,-1):
        print(page)
        url='http://www.nbd.com.cn/columns/3/page/'+str(page)+'.html'
        html = requests.get(url, headers=headers)
        Soup = BeautifulSoup(html.text, 'lxml')
        all_a = Soup.find_all('a', attrs={"href": re.compile(r'/articles/2017')})
        for a in all_a[::-1]:
            res_data['sid']=a['click-statistic']
            res_data['url'] = a['href']
            res_data['Title']=a.get_text()

            html1 = requests.get(res_data['url'], headers=headers)
            Soup1 = BeautifulSoup(html1.text, 'lxml')
            spans=Soup1.find('p',class_='u-time').find_all('span')

            res_data['source'] = spans[0].get_text().strip()
            res_data['time'] = spans[1].get_text().strip()

            abstract = Soup1.find('div',class_='g-article-abstract')
            if abstract is not None:

                res_data['sumary']=abstract.get_text().strip()
            else:
                res_data['sumary']=[]

            res_data['tags'] = []




            print(res_data['sid'],res_data['source'],res_data['time'],res_data['sumary'],res_data['Title'],res_data['tags'],res_data['url'])

           
            time.sleep(1)



        time.sleep(2)

getData()
