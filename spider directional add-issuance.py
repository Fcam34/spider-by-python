import time
import requests
import urllib.request
import json
import random
import re

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def getdata():
    for page in range(3,59):
        url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZF&st=5&sr=-1&p='+str(page)+'&ps=50&js=var%20irFGTOrV={pages:(pc),data:[(x)]}&stat=1&rt=49766633'
        response = urllib.request.urlopen(url).read().decode('utf-8')
        rex = re.compile(r"\[[^{}]*\]")
        data = rex.findall(response)
        ddata=''.join(data)
        con=json.loads(ddata)
        for d in con:
            arr1 = d.split(',')
            res_data = {
                'code':arr1[0],
                'number':arr1[3],
                'data':arr1[6]
            }
            href='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=ZFXX&code='+res_data['code']+'&stat=1&fd='+res_data['data']+'&cmd='+res_data['number']+''
            response1=urllib.request.urlopen(href).read().decode('utf-8')

            rex1 = re.compile(r"\[[^{}]*\]")
            data1 = rex1.findall(response1)
            ddata1 = ''.join(data1)
            con1 = json.loads(ddata1,strict=False)

            for c in con1:
                arr = c.split(',')
                res_data1 = {
                    '股票代码': arr[0],
                    '股票简称': arr[1],
                    '发行方式': arr[2],
                    '公开发行数量(万股)': arr[3],
                    '发行价格(元)': arr[4],
                    '发行日期': arr[5],
                    '增发上市日': arr[6],
                    '发行前总股本(万股)': arr[8],
                    '发行后总股本(万股)': arr[9],
                    '发行前每股净资产(元)': arr[10],
                    '发行后每股净资产(元)': arr[11],
                    '实际募集总额(万元)': arr[12],
                    '实际募集净额(万元)': arr[13],
                    '发行对象': arr[14],
                    '发行定价方式': arr[15]

                }
                print(res_data1['股票代码'], res_data1['股票简称'],res_data1['发行方式'],
                      res_data1['公开发行数量(万股)'],res_data1['发行价格(元)'],res_data1['发行日期'],
                      res_data1['增发上市日'],res_data1['发行前总股本(万股)'],res_data1['发行后总股本(万股)'],
                      res_data1['发行后总股本(万股)'],res_data1['发行前每股净资产(元)'],res_data1['发行后每股净资产(元)'],
                      res_data1['实际募集总额(万元)'],res_data1['实际募集净额(万元)'],res_data1['发行对象'],res_data1['发行定价方式'])

            time.sleep(5)


getdata()
