import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from lxml import html

url = 'https://fund.eastmoney.com/' #需要爬数据的网址

class get_names:
    
    def __init__(self,url):
        self.url = url
        self.names = []
        self.numbers = []
        
        self.get_url()
        self.name()
        self.number()
        self.tree = ''

    def get_url(self):
        page = requests.Session().get(self.url) 
        page.encoding = 'utf-8'
        self.tree = html.fromstring(page.text)

    def name(self):
        self.names = self.tree.xpath('//td[@class="ui-table-left"]//a/text()')
        
    def number(self):
        code = self.tree.xpath('//table[@class="ui-table ui-table-bordered-th-blank ui-table-hover ui-table-bordered-dashed"]//a/text()')
        for i in code:
            if len(i)==6 and i.isdigit()==True:
                self.numbers.append(i)
                
    def saves(self):
        for i in range(len(self.numbers)):
            df = ts.get_k_data(self.numbers[i]) 
            df.to_csv('股票.csv',header=None)
            data_0 = pd.read_csv('股票.csv',names=['日期','本日开始','本日结束','最高',' 最低','体积','代码'])
            data_0 = data_0.drop(['代码'],axis=1)
            data_0.to_csv(f'{self.names[i]}.csv',encoding="utf_8_sig",index=False)
            print(f"正在存储{self.names[i]}股票。。。")


def draw(path):
    data = pd.read_csv(path)
    
    x = data['日期']
    y = data['本日结束']

    #绘制折线图
    plt.rcParams['font.sans-serif']='SimHei'
    plt.figure(figsize=(10,6))
    plt.plot(x, y)
    plt.title('当日股票停盘')
    plt.xlabel('日期')
    plt.ylabel('股价')
    plt.show()

    #绘制饼状图
    plt.title('股票运势最高点分布(百分点)')
    label=['3.5以下','3.5-5','5-6.5','6.5以上']#定义饼图的标签，标签是列表
    explode=[0.01,0.01,0.01,0.01]#设定各项距离圆心n个半径
    values=[len(data[data['最高']<=0.7]),len(data[(data['最高'] >0.7 ) & (data['最高'] <=0.85)]),len(data[(data['最高'] >0.85 ) & (data['最高'] <=1)]),len(data[data['最高'] > 1])]

    plt.pie(values,explode=explode,labels=label,autopct='%1.1f%%',radius=2)#绘制饼图
    plt.show()

    #绘制柱状图
    data.hist('本日开始')
    plt.show()
    
if __name__ == '__main__':
    start = get_names(url)
    start.saves()
    #draw(国投瑞银白银期货(LOF).csv)