import requests
from bs4 import BeautifulSoup
import os

headers = { 'User-Agent': "Mozilla/5.0(x11;Linux x86_64;rv:38.0) Gecko/20100101 Firefox/38.0 Iceweasel/38.3.0"}
all_url = 'http://www.mzitu.com/all'
start_html = requests.get(all_url,headers=headers)
Soup = BeautifulSoup(start_html.text, 'lxml')
all_a = Soup.find('div', class_='all').find_all('a')
for a in all_a:
    title = a.get_text()
    path = str(title).strip()
    os.makedirs(os.path.join("E:\爬虫图库1", path))
    os.chdir("E:\爬虫图库1\\" + path)
    href = a['href']
    html = requests.get(href, headers=headers)
    html_Soup = BeautifulSoup(html.text, 'lxml')
    max_span = html_Soup.find('div', class_='pagenavi').find_all('span')[-2].get_text()
    for page in range(1, int(max_span) + 1):
        page_url = href + '/' + str(page)
        img_html = requests.get(page_url, headers=headers)
        img_Soup = BeautifulSoup(img_html.text, 'lxml')
        img_url = img_Soup.find('div', class_='main-image').find('img')['src']
        name = img_url[-9:-4]
        img = requests.get(img_url, headers=headers)
        f = open(name + '.jpg', 'ab')
        f.write(img.content)
        f.close()
