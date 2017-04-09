import json
import sys
import re
import time
from bs4 import BeautifulSoup
from lib.common.utils import Utils
from lib.db.mysql import DbMysql

reload_num = 0
		is_proxy = False
		cookie = 'JSESSIONID=0000-AVnS-7o-1leumTUkpLUnEt:-1'
		page = 1 #81
		headers = {}
		def __init__(self,saveTableName):
			# lists = self.findAllLimitAndSort(saveTableName,{'status':0},0,10)
			# print(lists)
			# return
			self.saveTableName = saveTableName
			self.headers = {
				'Accept':'application/json, text/javascript, */*; q=0.01',
				'Accept-Language':'zh-CN,zh;q=0.8',
				'Cache-Control':'no-cache',
				'Connection':'keep-alive',
				'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
				'DNT':'1',
				'Host':'www.chinawealth.com.cn',
				'Pragma':'no-cache',
				'Referer':'http://www.chinawealth.com.cn/zzlc/jsp/lccp.jsp',
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
				'X-Requested-With':'XMLHttpRequest',
				'Cookie':self.cookie
			}
			self.getData()


		def getData(self):
			self.setLog('page:' + str(self.page))
			if(self.page < 1 or self.reload_num > 2):
				sys.exit()
			url = "http://www.chinawealth.com.cn/lccpAllProJzyServlet.go"
			postData = {
				'pagenum':self.page,
				'tzzlxdm':'03',
				'cpzt':'02,04',
				# 'cpjglb':'01'	#机构类别：01国有银行，02股份制银行，03城商行，04外资银行，05农村合作金融机构，00,06,07,08,09其他
			}
			html_doc = Utils.curlPost(url,postData,self.headers,self.is_proxy,True)
			cookies = Utils.getCookie(html_doc['header'])
			print('newcookies:' + cookies)
			self.cookie = cookies
			# print(html_doc)
			if(html_doc['content'] == None or len(html_doc['content']) == 16):
				self.setLog('getData:' + html_doc['content'])
				self.reload_num += 1
				self.getData()
				return


			data = json.loads(html_doc['content'])

			try:
				lists = data['List']
				self.save(lists)
				# return
				self.page -=1
				time.sleep(15)
				self.getData()
			except:
				self.setLog('getData not List' + str(len(html_doc['content'])))
				self.reload_num += 1
				self.getData()
				return




		def getCpIdArea(self,cpid):
			if(self.reload_num > 2):
				sys.exit()
			time.sleep(10)
			url = 'http://www.chinawealth.com.cn/cpxsqyQuery.go'
			self.setLog(url + "--" + str(cpid))
			postData = {
				'pagenum':1,
				'tzzlxdm':'03',
				'cpid':cpid
			}
			html_doc = Utils.curlPost(url,postData,self.headers,self.is_proxy,True)
			cookies = Utils.getCookie(html_doc['header'])
			self.cookie = cookies
			self.setLog("new cookies:" + cookies)
			data = json.loads(html_doc['content'])

			try:
				cpNameList = []
				for v in data['List']:
					cpNameList.append(v['cpxsqy'])
				cpNames = ','.join(cpNameList)
				return cpNames
			except:
				print('getCpIdArea not in a_list')
				self.reload_num += 1
				return getCpIdArea(cpid)


		def save(self,data):
			for d in data[::-1]:
				uniqueId = self.getMd5(d['cpid'])
				res_data = {}
				res_data['uniqueId'] = uniqueId
				resOne = self.getUniqueId(self.saveTableName,res_data)
				if(resOne != None):
					return


			
				res_data = {
					'cpid':d['cpid'],
					'产品名称':d['cpms'],
					'产品类别':d['tzzlxms'],
					'登记编码':d['cpdjbm'],
					'发行机构':d['fxjgms'],
					'产品状态':d['cpztms'],					
					'运作模式':d['cplxms'],
					'风险等级':d['fxdjms'],
					'期限类型':d['qxms'],
					'募集起始日期':d['mjqsrq'],
					'募集结束日期':d['mjjsrq'],
					'产品起始日期':d['cpqsrq'],
					'产品终止日期':d['cpyjzzrq'],
					'业务起始日':d['kfzqqsr'],
					'业务结束日':d['kfzqjsr'],
					'收益类型':d['cpsylxms'],
					'募集币种':d['mjbz'],
					'起点销售金额':d['qdxsje'],
					'初始净值':d['csjz'],
					'产品净值':d['cpjz'],
					'预期最低收益率':d['yjkhzdnsyl'],
					'预期最高收益率':d['yjkhzgnsyl'],
					'实际天数':d['cpqx'],
					'到期实际收益率':d['dqsjsyl'],
					'投资资产类型':d['tzlxms'],
					'销售区域':'',
					'status':0
				}
				res_data['add_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
				self.insertData(self.saveTableName,res_data)
				sql = 'INSERT INTO `lccp` (`cpid`, `cpms`,`tzzlxms`,`cpdjbm`,`fxjgms`,`cpztms`,`cplxms`,`fxdjms`,`qxms`,`mjqsrq`,`mjjsrq`,`cpqsrq`,`cpyjzzrq`,`kfzqqsr`,`kfzqjsr`,`cpsylxms`,`mjbz`,`qdxsje`,`csjz`,`cpjz`,`yjkhzdnsyl`,`yjkhzgnsyl`,`cpqx`,`dqsjsyl`,`tzlxms`,`area`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
				data = (res_data['cpid'], res_data['产品名称'], res_data['产品类别'], res_data['登记编码'], res_data['发行机构'],
						res_data['产品状态'], res_data['运作模式'], res_data['风险等级'], res_data['期限类型'],
						res_data['募集起始日期'], res_data['募集结束日期'], res_data['产品起始日期'], res_data['产品终止日期'],
						res_data['业务起始日'], res_data['业务结束日'], res_data['收益类型'], res_data['募集币种'], res_data['起点销售金额'],
						res_data['初始净值'], res_data['产品净值'], res_data['预期最低收益率'],
						res_data['预期最高收益率'], res_data['实际天数'], res_data['到期实际收益率'], res_data['投资资产类型'],
						res_data['销售区域'])
				DbMysql().executeCommit(sql, data)
