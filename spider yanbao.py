import requests
from bs4 import BeautifulSoup
import re
import urllib.request
import time
import os



headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

for page in range(1, 3):
    url = 'http://www.hibor.com.cn/microns_1_'+str(page)+'.html'
    html = requests.get(url, headers=headers)

    Soup = BeautifulSoup(html.text, 'lxml')

    all_td = Soup.find_all('a', attrs={"href": re.compile(r'^/docdetail')})
    for td in all_td[::2]:
        res_data = {}
        href = 'http://www.hibor.com.cn'+td['href']
        str1=td['href']
        rex1= re.compile(r'\d+')
        List=rex1.findall(str1)
        str2=''.join(List)
        #print(str2)
        #print(href)
        res_data['title'] = td.get_text()
        html1 = requests.get(href, headers=headers)
        html1.encoding = 'gbk'
        Soup = BeautifulSoup(html1.text, 'lxml')


        spans=Soup.find('table',class_='btab').find_all('span')
        res_data['name']=spans[0].get_text()
        res_data['code']=spans[1].get_text()
        res_data['time'] = spans[2].get_text()
        res_data['line'] = spans[3].get_text()
        res_data['kind'] = spans[5].get_text()
        res_data['author'] = spans[6].get_text()
        res_data['where'] = spans[7].get_text()
        res_data['page'] = spans[8].get_text()
        res_data['level'] = spans[9].get_text()
        res_data['download']='http://www.hibor.com.cn/webdownload.asp?uname=lenhaibo&did='+str(str2)+'&degree=1&baogaotype=1&fromtype=21'
        res_data['pdfurl']='http://www.hibor.com.cn/webpdf.asp?&uname=lenhaibo&did='+str(str2)+'&degree=1&baogaotype=1&fromtype=21'


        print(res_data['title'],'\t',res_data['name'],res_data['code'],res_data['time'],res_data['line'],res_data['kind'],res_data['author'],
              res_data['where'],res_data['level'], res_data['download'],'\t',res_data['pdfurl'])

        cookie = {***********
                 *************} #登陆后的cookie
        r = requests.post(res_data['download'], cookies=cookie)
        #d = requests.get(res_data['download'])
        with open(res_data['title']+'.pdf', "wb") as code:
            code.write(r.content)


        time.sleep(10)
