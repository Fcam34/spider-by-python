import json
import sys
import re
import time
from lib.common.utils import Utils
from bs4 import BeautifulSoup
from lib.db.mysql import DbMysql


#大宗交易
#http://data.eastmoney.com/dzjy/2017.html

page = 2013
saveTableName = None
def __init__(self,saveTableName):
	self.saveTableName = saveTableName
	self.getData()


def getData(self):
	

	localtime = time.localtime(time.time())
	tm_year = localtime.tm_year
	tm_mon = localtime.tm_mon
	if(tm_mon < 10):
		tm_mon = "0" + str(tm_mon)
	self.page = str(tm_year) + str(tm_mon)

	url = "http://data.eastmoney.com/dzjy/" + str(self.page) + ".html"
	html_doc = Utils.curlGet(url).decode("gbk")
	soup = BeautifulSoup(html_doc, "html.parser")

	trList = soup.find('div',id = 'content').find_all('div',class_="list")[2].find_all('tr',class_="list_eve")
	thisTime = None
	thisCode = None
	thisCodeName = None
	thisPrice = None

	for tr in trList:
		tds = tr.find_all('td')
		startIndex = 0
		if(len(tds) == 10):
			thisTime = tds[0].get_text()
			startIndex +=1

	 if(len(tds) >= 9):
			res_data = {}
			res_data['交易日期'] = thisTime
			res_data['股票代码'] = thisCode = tds[startIndex].get_text()
			res_data['股票简称'] = thisCodeName = tds[startIndex+1].get_text()
			res_data['当前价格'] = thisPrice = tds[startIndex+3].get_text()
			res_data['成交价格'] = tds[startIndex+4].get_text()
			res_data['成交数量'] = tds[startIndex+5].get_text()
			res_data['成交金额'] = tds[startIndex+6].get_text()
			res_data['买方营业部'] = tds[startIndex+7].get_text()
			res_data['卖方营业部'] = tds[startIndex+8].get_text()
				
	 if(len(tds) == 5):
			res_data = {}
			res_data['交易日期'] = thisTime
			res_data['股票代码'] = thisCode
			res_data['股票简称'] = thisCodeName
			res_data['当前价格'] = thisPrice
			res_data['成交价格'] = tds[startIndex].get_text()
			res_data['成交数量'] = tds[startIndex+1].get_text()
			res_data['成交金额'] = tds[startIndex+2].get_text()
			res_data['买方营业部'] = tds[startIndex+3].get_text()
			res_data['卖方营业部'] = tds[startIndex+4].get_text()

		self.save(res_data)





def save(self,res_data):
		


	self.saveData(self.saveTableName,res_data)

	sql = 'INSERT INTO `dzjy` (`time`, `code`,`Codename`,`Pricenow`,`Price`,`number`,`money`,`buy`,`sell`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)'
	data = (res_data['交易日期'],res_data['股票代码'],res_data['股票简称'],res_data['当前价格'],res_data['成交价格'],res_data['成交数量'],res_data['成交金额'],res_data['买方营业部'],res_data['卖方营业部'])
	DbMysql().executeCommit(sql, data)

