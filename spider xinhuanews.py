from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import json
import random
import re


headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def getData():


    url = 'http://qc.wa.news.cn/nodeart/list?nid=11147664&pgnum=1&cnt=100&tp=1&orderby=1?callback=jQuery1710010292672309485162_1492415463549&_=1492415463682'
#   财经


#    url='http://qc.wa.news.cn/nodeart/list?nid=113352&pgnum=1&cnt=100&tp=1&orderby=1?callback=jQuery1113004577009162556145_1492504430874&_=1492504430875'
#   时政

    response=urllib.request.urlopen(url).read().decode('utf-8')
    #print(response)
    rex=re.compile(r'\w+[(]{1}(.*)[)]{1}')   #正则表达式
    data=rex.findall(response)
    #print(data)
    con=''.join(data)
    #print(con)

    ddata=json.loads(con)

    #print(type(ddata))

    List=ddata['data']
    for a in range(0,99):



        res_data = {}
        res_data['DocID'] = List['list'][a]['DocID']
        res_data['Title'] = List['list'][a]['Title']
        res_data['NodeId'] = List['list'][a]['NodeId']
        res_data['PubTime'] = List['list'][a]['PubTime']
        res_data['LinkUrl'] = List['list'][a]['LinkUrl']
        res_data['Abstract'] = List['list'][a]['Abstract']
        res_data['keyword'] = List['list'][a]['keyword']
        res_data['Editor'] = List['list'][a]["Editor"]
        res_data['Author'] = List['list'][a]['Author']
        res_data['SourceName'] = List['list'][a]['SourceName']

        print(res_data['DocID']+'\t'+res_data['Title']+'\t'+res_data['LinkUrl']+'\t'+res_data['Abstract'])




getData()
