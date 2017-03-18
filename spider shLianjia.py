import requests
from bs4 import BeautifulSoup
import re

for page in range(1,100):
    all_url='http://sh.lianjia.com/chengjiao/d'+str(page)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

    start_html = requests.get(all_url,  headers=headers)
    Soup=BeautifulSoup(start_html.text,'lxml')
    all_a = Soup.find('ul',class_='clinch-list').find_all( 'a',attrs={"href": re.compile(r'html*$')})

    for a in all_a:
        all_url = 'http://sh.lianjia.com'+a['href']
        start_html = requests.get(all_url, headers=headers)
        Soup = BeautifulSoup(start_html.text, 'lxml')
        a = Soup.find('table', class_='aroundInfo')

        title2 = a.get_text()
        print(title2)
        print('---------------------------------------------')
