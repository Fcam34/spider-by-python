import urllib.request
import re
import random
import time

forex_total=[]
for page in range(1,4):#抓取数据的页码
    url='http://quote.stockstar.com/forex/all_3_1_'+str(page)+'.html'#目标网址
    request=urllib.request.Request(url=url,headers={"User-Agent":'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'})
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
    forex_page=re.findall(pattern,body[0])
    forex_total.extend(forex_page)
    time.sleep(random.randrange(1,4))

forex_last=forex_total[:]
for data in forex_total:
    if data=='':
        forex_last.remove('')
#打印部分结果
print('代码','\t','名称','   ','\t','     最新价','\t','  涨跌幅','\t','   开盘','\t','  最高','\t','  最低' ,'\t','  昨入','\t',' 买入','\t','  卖出')
for i in range(0,len(forex_last),10): #网页数据有10列
    print(forex_last[i],'\t',forex_last[i+1],' ','\t',forex_last[i+2],'  ','\t',forex_last[i+3],'  ','\t',forex_last[i+4],'  ','\t',forex_last[i+5],'  ','\t',forex_last[i+6],'\t',forex_last[i+7],'\t',forex_last[i+8],'\t',forex_last[i+9])
