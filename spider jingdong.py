#-*-coding:utf-8-*-
from bs4 import BeautifulSoup
import time
import requests
import urllib.request
import json
import re

#京东

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
res_data = {}
def getData():
    for page in range(1,100,1):
        url='https://list.jd.com/list.html?cat=670,671,672&page='+str(page)+'&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'
        html = requests.get(url, headers=headers)
        Soup = BeautifulSoup(html.text, 'lxml')
        hrefs=Soup.find('ul',class_='gl-warp clearfix ').find_all('a', attrs={"href": re.compile(r'//item.jd.com/')})
        for a in hrefs[::2]:

            res_data['href']='http:'+a['href']
            html = requests.get(res_data['href'], headers=headers)
            Soup1 = BeautifulSoup(html.text, 'lxml')
            info=Soup1.find('div',class_='sku-name')
            res_data['computer']=info.get_text().strip()

            mode = re.compile(r'\d+')
            sid=mode.findall(res_data['href'])
            res_data['sid']=''.join(sid)

            url1='https://p.3.cn/prices/mgets?&type=1&area=1_72_4137_0&pdtk=&pduid=219400153&pdpin=&pdbp=0&skuIds=J_'+str(res_data['sid'])
            response = urllib.request.urlopen(url1).read().decode('utf-8')

            res=re.compile('\{.*?\}' )

            ddata=res.findall(response)

            con = ''.join(ddata)
            data = json.loads(con)

            res_data['money']=data['p']
            res_data['price']=data['m']
            a=float(data['p'])
            b=float(data['m'])
            res_data['diff']=str(b-a)


            print(res_data['sid'],res_data['href'], res_data['computer'],'￥'+res_data['money'],'￥'+res_data['price'],'￥'+res_data['diff'])





getData()

