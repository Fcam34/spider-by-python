import requests
from bs4 import BeautifulSoup
import re
import time
import csv

info={}

fileHeader = ["房源编码", "标题","图片","链接","租金","类型","大小","位置","朝向","区域","小区","地址","带看次数","挂牌时间","爬取时间"]
csvFile = open("C:/Users/ThinkPad/Desktop/新建文件夹/instance.csv", "w")
writer = csv.writer(csvFile)
writer.writerow(fileHeader)
csvFile.close()

for page in range(1,100):
    print(page)
    all_url='http://sh.lianjia.com/zufang/d'+str(page)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    start_html = requests.get(all_url,  headers=headers)
    Soup=BeautifulSoup(start_html.text,'lxml')
    #print(Soup)
    all_a = Soup.find('ul',class_='house-lst js_fang_list').find_all( 'a',attrs={"href": re.compile(r'/zufang/shz')})

    for a in all_a[::2]:
        url = 'http://sh.lianjia.com'+a['href']
        info['url']=url

        html=requests.get(url,headers=headers)
        Soup1 = BeautifulSoup(html.text, 'lxml')
        info['title']=Soup1.find('h1',class_='main')['title']
        info['pic']=Soup1.find('img')['src']
        info['price']=Soup1.find('div',class_='price').get_text().strip()
        info['room']=Soup1.find('div',class_='room').get_text().strip()
        info['area']=Soup1.find('div',class_='area').get_text().strip()
        floor=Soup1.find_all('td',width='50%')[0].get_text().strip()
        info['floor']=re.sub('  ','',floor)
        forword=Soup1.find_all('td',width='50%')[1].get_text().strip()
        info['forword']=re.sub('  ','',forword)
        where = Soup1.find_all('td', width='50%')[2].get_text().strip()
        info['where'] = re.sub('  ', '', where)
        when=Soup1.find_all('td',width='50%')[3].get_text().strip()
        info['when']=re.sub('  ','',when)
        info['xiaoqu']=Soup1.find_all('p',class_='addrEllipsis')[0]['title']
        info['address']=Soup1.find_all('p',class_='addrEllipsis')[1]['title']

        info['id']=re.sub('房源编号：','',Soup1.find('span',class_='houseNum').get_text().strip())
        info['look']=Soup1.find('div',class_='totalCount').get_text().strip()



        timenow=time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

        data=[info['id'],info['title'],info['pic'],info['url'],info['price'],info['room'],info['area'],info['floor'],info['forword'],info['where'],info['xiaoqu'],info['address'],info['look'],info['when'],timenow]

        csvFile = open("C:/Users/ThinkPad/Desktop/新建文件夹/instance.csv", "a")
        writer = csv.writer(csvFile)
        writer.writerow(data)


        print(info['id'],info['title'],info['pic'],info['url'],info['price'],info['room'],info['area'],info['floor'],info['forword'],info['where'],info['xiaoqu'],info['address'],info['look'],info['when'],timenow)

        time.sleep(6)
        csvFile.close()
