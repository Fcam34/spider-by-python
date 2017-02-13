import urllib.request
import re
import random
import time

#抓取所需内容

user_agent = ["Mozilla/5.0 (Windows NT 10.0; WOW64)", 'Mozilla/5.0 (Windows NT 6.3; WOW64)',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
            ]
stock_total=[]
for page in range(1,3):#抓取数据的页码
    url='http://quote.stockstar.com/forex/all_3_1_'+str(page)+'.html'
    request=urllib.request.Request(url=url,headers={"User-Agent":random.choice(user_agent)})
    try:
        response=urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:            #异常检测
        print('page=',page,'',e.code)
    except urllib.error.URLError as e:
        print('page=',page,'',e.reason)
    content=response.read().decode('gbk')       #读取网页内容
    print('get page',page)                  #打印成功获取的页码
    pattern=re.compile('<tbody[\s\S]*</tbody>')
    body=re.findall(pattern,str(content))
    pattern=re.compile('>(.*?)<')               #正则表达式进行正则匹配
    stock_page=re.findall(pattern,body[0])
    stock_total.extend(stock_page)
    time.sleep(random.randrange(1,4))        
                                            #数值可根据实际情况改动
stock_last=stock_total[:]
for data in stock_total:
    if data=='':
        stock_last.remove('')
#打印部分结果
print('代码','\t','名称','   ','\t','     最新价','\t','  涨跌幅','\t','   开盘','\t','  最高','\t','  最低')
for i in range(0,len(stock_last),10): #网页数据有10列
    print(stock_last[i],'\t',stock_last[i+1],' ','\t',stock_last[i+2],'  ','\t',stock_last[i+3],'  ','\t',stock_last[i+4],'  ','\t',stock_last[i+5],'  ','\t',stock_last[i+6])
