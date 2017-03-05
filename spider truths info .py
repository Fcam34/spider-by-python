from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import time

#爬取网站所有信托信息

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
driver = webdriver.PhantomJS(executable_path='C:/Users/admin/Downloads/phantomjs-windows/phantomjs-2.1.1-windows/bin/phantomjs')
all_url = 'http://www.yanglee.com/product/product.html'
driver.get(all_url)
for page in range(0,218):
    web_data = driver.page_source
    Soup = BeautifulSoup(web_data, 'lxml')
    time.sleep(2)
    all_a = Soup.find_all('a', attrs={"href": re.compile(r'^product_detail')})
    print(page)
    for a in all_a:
        a_url = 'http://www.yanglee.com/product/' + a['href']

        second_html = requests.get(a_url, headers=headers)
        Soup = BeautifulSoup(second_html.text, 'lxml')
        all_td = Soup.find('div', class_='pro_2').find_all('td')

        print('---------------------------------------------------------------------------------------------------')
        for td in all_td:
            title = td.get_text()
            print(title)
    driver.find_element_by_xpath("//a[contains(text(),'下一页')]").click()  #模拟浏览器实现翻页
    page=page+1
