import cmath
from BitVector import BitVector
import requests
from bs4 import BeautifulSoup
import re
import csv

# 利用布隆过滤器完成去重，提取要求信息，输入csv

csvFile = open('C:/Users/admin/Desktop/truths/money.csv', 'wt', encoding='utf-8')  # 创建csv文件位置
writer = csv.writer(csvFile)

# 布隆过滤器

class BloomFilter(object):
    def __init__(self, error_rate, elementNum):  # 计算所需要的bit数
        self.bit_num = -1 * elementNum * cmath.log(error_rate) / (cmath.log(2.0) * cmath.log(2.0))    # 四字节对齐
        self.bit_num = self.align_4byte(self.bit_num.real) # 分配内存
        self.bit_array = BitVector(size=self.bit_num)   # 计算hash函数个数
        self.hash_num = cmath.log(2) * self.bit_num / elementNum
        self.hash_num = self.hash_num.real  # 向上取整
        self.hash_num = int(self.hash_num) + 1  # 产生hash函数种子
        self.hash_seeds = self.generate_hashseeds(self.hash_num)

    def insert_element(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed) # 取绝对值
            hash_val = abs(hash_val)  # 取模，防越界
            hash_val = hash_val % self.bit_num # 设置相应的比特位
            self.bit_array[hash_val] = 1

    #检查元素是否存在，存在返回1，否则返回0
    def is_element_exist(self, element):
        for seed in self.hash_seeds:
            hash_val = self.hash_element(element, seed)
            hash_val = abs(hash_val) # 取模，防越界
            hash_val = hash_val % self.bit_num  # 查看值
            if self.bit_array[hash_val] == 0:
                return 0
        return 1

    #内存对齐
    def align_4byte(self, bit_num):
        num = int(bit_num / 32)
        num = 32 * (num + 1)
        return num

    #产生hash函数种子,hash_num个素数
    def generate_hashseeds(self, hash_num):
        count = 0 # 连续两个种子的最小差值
        gap = 50 # 初始化hash种子为0
        hash_seeds = []
        for index in range(hash_num):
            hash_seeds.append(0)
        for index in range(10, 10000):
            max_num = int(cmath.sqrt(1.0 * index).real)
            flag = 1
            for num in range(2, max_num):
                if index % num == 0:
                    flag = 0
                    break

            if flag == 1: # 连续两个hash种子的差值要大才行
                if count > 0 and (index - hash_seeds[count - 1]) < gap:
                    continue
                hash_seeds[count] = index
                count = count + 1

            if count == hash_num:
                break
        return hash_seeds

    def hash_element(self, element, seed):
        hash_val = 1
        for ch in str(element):
            chval = ord(ch)
            hash_val = hash_val * seed + chval
        return hash_val

# 获取所有详情链接，去除重复，爬取所有信息

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
j = 2013
while j < 2018:
    for i in range(1, 13):
        data = j*100+i
        a_url = 'http://data.eastmoney.com/dzjy/' + str(data)+ '.html' # 获取2013.1—2017.12的所有网页链接
        html = requests.get(a_url, headers=headers)
        Soup = BeautifulSoup(html.text, 'lxml')
        all_a = Soup.find_all('a', attrs={"href":re.compile(r'^/dzjy/detail')})
        bf = BloomFilter(0.001, 1000000)
        element = '0'
        bf.insert_element(element)
        for a in all_a:
            href = a['href']

            B = bf.is_element_exist(href)  # 获取所有关于详情的链接，并判断是否已经存在
            if B == 0:
                bf.insert_element(href)   # 导入不存在的链接
                aim_url = 'http://data.eastmoney.com' + href
                aim_html = requests.get(aim_url, headers=headers)
                Soup = BeautifulSoup(aim_html.text, 'lxml')
                tr_all = Soup.find_all('tr', class_='list_eve')

                csvRow = []
                name = []
                name_all = Soup.find('div', class_='msg')
                name.append(name_all.get_text())
                writer.writerow(name)

                info_all = Soup.find('tr', class_='subhead')
                info = info_all.get_text()
                csvRow.append(info)

                for tr in tr_all:
                    csvRow.append(tr.get_text())

                writer.writerow(csvRow)

        i=i+1
    j=j+1
