import urllib.request
import json
import random
import re
import time

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def getData():

    url='http://3g.163.com/touch/article/list/BA8EE5GMwangning/0-1000.html'
    response = urllib.request.urlopen(url).read().decode('utf-8')
    rex = re.compile(r'\w+[(]{1}(.*)[)]{1}')
    data = rex.findall(response)
    con = ''.join(data)
    ddata = json.loads(con)

    for a in range(0,999):
        res_data = {}
        res_data['docid'] = ddata['BA8EE5GMwangning'][a]['docid']
        res_data['title'] = ddata['BA8EE5GMwangning'][a]['title']
        res_data['source'] = ddata['BA8EE5GMwangning'][a]['source']
        res_data['ptime'] = ddata['BA8EE5GMwangning'][a]['ptime']
        res_data['url'] = ddata['BA8EE5GMwangning'][a]['url']
        res_data['digest'] = ddata['BA8EE5GMwangning'][a]['digest']

        print(res_data['docid']+'\t'+res_data['title']+'\t'+res_data['source']+'\t'+res_data['ptime']+'\t'+res_data['url'])



getData()
