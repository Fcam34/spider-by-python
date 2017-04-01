import json
import sys
import re
import time
from lib.common.utils import Utils
from lib.db.mysql import DbMysql



page = 1
saveTableName = None
def __init__(self,saveTableName):
	self.saveTableName = saveTableName
	self.getData()
			
			
def getData(self):
	print(self.page)
	if(self.page < 1):
		sys.exit()
	url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GG&sty=GGMX&p=" + str(self.page) + "&ps=100&js=var%20aciVeuVJ={pages:(pc),data:[(x)]}&rt=49668746"
	html_doc = Utils.curlGet(url).decode("utf-8")
			
	html_len = len(html_doc)
	page_index = html_doc.find('pages')
	page_end_index = html_doc.find(',')
	pages = html_doc[page_index+6:page_end_index]
			
		

	if(page_index == -1):
		sys.exit()

	data_index = html_doc.find('data')
	data_end_index = html_doc.rfind(']')

	json_data = html_doc[data_index + 5:data_end_index + 1]
	data = json.loads(json_data)
	if(len(data) <= 0):
		sys.exit()


	self.save(data)
	self.page -= 1
	time.sleep(10)
	self.getData()


def save(self,data):
	for d in data[::-1]:
			
		arr = d.split(',')
		res_data = {
			'日期':arr[5],
			'股票代码':arr[2],
			'股票名称':arr[9],
			'变动人':arr[3],
      '变动股数':arr[6],
			'成交均价':arr[8],
      '变动金额(万)':arr[13],
			'变动原因':arr[12],
      '变动比例(%)':arr[0],
			'变动后持股数':arr[7],
			'持股种类':arr[4],
			'董监高人员姓名':arr[1],
			'职务':arr[14],
			'变动人与董监高的关系':arr[10]
		}
		self.saveData(self.saveTableName,res_data)
		sql = 'INSERT INTO `ggzjc` (`data`, `code`,`codename`,`name`,`number`,`price`,`money`,`reason`,`radio`,`numberaft`,`style`,`namehigh`,`job`,`relationship`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		data = (res_data['日期'], res_data['股票代码'], res_data['股票名称'], res_data['变动人'], res_data['变动股数'],
						res_data['成交均价'], res_data['变动金额(万)'], res_data['变动原因'], res_data['变动比例(%)'],
						res_data['变动后持股数'], res_data['持股种类'], res_data['董监高人员姓名'], res_data['职务'],
						res_data['变动人与董监高的关系'])
		DbMysql().executeCommit(sql, data)
