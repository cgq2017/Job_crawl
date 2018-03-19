# coding=utf-8
from bs4 import BeautifulSoup
import urllib.request
import requests
from lxml import etree
import csv
import os

def craw_data(url):
    '''数据抓取'''
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    # }
    #
    # html = requests.get(url)
    # html = html.text.encode(html.encoding)
    # s = etree.HTML(html)
    s=startcraw(url)
    for i in range(50):
        tr = '//*[@id="resultList"]/div{}'.format([i+4])
        if(len(s.xpath(tr + '/p/span/a/text()'))==0):
            title=' '
        else:
            title = s.xpath(tr + '/p/span/a/text()')[0].strip()
        if(len(s.xpath(tr + '/span[1]/a/text()'))==0):
            company=' '
        else:
            company = s.xpath(tr + '/span[1]/a/text()')[0].strip()
        if(len(s.xpath(tr + '/span[2]/text()'))==0):
            destination=' '
        else:
            destination = s.xpath(tr + '/span[2]/text()')[0].strip()
        if(len(s.xpath(tr+'/p/span/a/@href'))==0):
            herf=' '
            infomation=' '
        else:
            herf=s.xpath(tr+'/p/span/a/@href')[0].strip()
            s1=startcraw(herf)
            # infomation=' '.join(s1.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()'))
            # if(len(s1.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()'))==0):
            #     infomation=' '

                # for i in range(len(s1.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()'))):

            infomation = ' '.join(s1.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/text()')).strip()
            infomation.replace(' ', '')
            if(len(infomation)==0):
                infomation = ' '.join(s1.xpath('/html/body/div[3]/div[2]/div[3]/div[2]/div/p/text()')).strip()
                infomation.replace(' ', '')
        if(len(s.xpath(tr + '/span[3]/text()'))==0):
            money= " "
        else:
            money = s.xpath(tr + '/span[3]/text()')[0].strip()
        title_.append(title)
        company_.append(company)
        destination_.append(destination)
        money_.append(money)
        href_.append(herf)
        information_.append(infomation)
        print(title, company, destination,money,herf,infomation,len(infomation))


# craw_data(url)
def getUrl():
    for i in range(1):
        url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,{}.html?'.format(i+1)
        craw_data(url)
    excel()
def excel():
    filename = r'terminal_mlp6.csv'
    if os.path.exists(filename):
        print("filename exists!")
    else:
        fobj = open("terminal_mlp6.csv", 'w',newline='',encoding='gbk')

        write_f = csv.writer(fobj)
        write_f.writerow(('招聘标题', '公司名称','工作地点','薪资','链接','工作内容'))
        for i in range(len(money_)):

             write_f.writerow((title_[i],company_[i],destination_[i],money_[i],href_[i],information_[i].replace(u'\xa0 ', u' ')))
        fobj.close()
def startcraw(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    }
    html = requests.get(url)

    html = html.text.encode(html.encoding)

    # html = html.text.encode('ios-8859-1').decode('gbk')
    s = etree.HTML(html)
    return s

title_=[]
company_=[]
destination_=[]
money_=[]
href_=[]
information_=[]
getUrl()
