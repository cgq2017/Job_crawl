import re
import requests
from bs4 import BeautifulSoup
from lxml import etree

def craw_spider(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    }
    html=requests.get(url,headers=headers)
    html=html.text.encode(html.encoding).decode('gbk')
    # html=html.encode(html.encoding)
    # m=BeautifulSoup(html,'lxml')
    # m=etree.HTML(html)
    # print(html)
    return html
def get_information(url):
    html=craw_spider(url)
    s=re.findall('<a target="_blank" title="(.*?)" href="(.*?)">',html,re.S)
    s1=re.findall('<span class="t3">(.*?)<',html,re.S)[1:]
    s2 = re.findall('<span class="t4">(.*?)<', html, re.S)[1:]
    m=s[::2]
    m1=s[1::2]
    s = re.findall('<a target="_blank" title="(.*?)" href="(.*?)">', html, re.S)

    for i in range(len(s1)):
        print(m[i][0],m1[i][0],s1[i],m[i][1].split('"')[0],s2[i])
        title.append(m[i][0])
    print(len(title))






def get_url():
    for i in range(1000):
        url='http://search.51job.com/list/000000%252C00,000000,0000,00,9,99,%2B,2,{}.html?'.format(i+1)
        get_information(url)
title=[]
company=[]
destination=[]
herf=[]
money=[]
# get_information('http://jobs.51job.com/guangzhou-thq/99748341.html?s=01&t=0')
get_url()