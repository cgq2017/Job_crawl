
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import urllib.response
import time
import csv
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
def craw_spider(url):
    '''网页获取'''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 QIHU 360SE'
    }
    # html=urlopen(url)
    session=requests.Session()
    html=session.get(url,headers=headers)
    html=html.text.encode(html.encoding)
    html=html.decode('gbk')
    bsobi=BeautifulSoup(html,'lxml')

    return bsobi

def get_information(url):
    '''爬取信息'''
    try:
        m = craw_spider(url)
    except:
        time.sleep(1)
        m = craw_spider(url)
    g = m.find('div', {'id': 'resultList'}).find_all('div', {'class': "el"})[1:]
    a=[]
    for i in range(len(g)):
        g1 = g[i].findAll('a')
        # m=''.join(g[i].get_text().strip().split('\n'))
        m = g[i].get_text().strip().split('\n')
        title.append(m[0].strip())
        company.append(m[-4].strip())
        destination.append(m[-3].strip())
        money.append(m[-2].strip())
        href = g1[0].attrs['href']
        hef.append(href)
        print(m, href)
        try:
            content_work = craw_spider(g1[0].attrs['href'])
        except:
            try:
                time.sleep(1)
                content_work = craw_spider(g1[0].attrs['href'])
            except:
                content_work=''
        try:
            if(len(content_work)==0):
                work_information=' '
            else:
                w = content_work.find('div', {'class': 'bmsg job_msg inbox'})
                work_information = ''.join(w.get_text()).strip().split('\n')[0]
                if(len(work_information)==0):
                    work_information= '  '
        except:
            work_information = '  '
        print(work_information)
        information.append(work_information)



def start_auto():
    '''翻页，对每一页爬取'''
    for i in range(2000):
        url = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%2B,2,{}.html?'.format(i+1)
        try:
            get_information(url)
        except:
            try:
                time.sleep(2)
                get_information(url)
            except:
                mail("爬虫由于某种原因中断了，{}页出现问题,链接为{}".format(i,url))
    excel()



def excel():
    '''数据写入'''
    file_name=open('bs5_qianchengwuyou.csv','w',newline='',encoding='gbk')
    write_f=csv.writer(file_name)
    write_f.writerow(("招聘标题", '公司名称', '工作地点', '薪资', '链接','工作内容'))
    for i in range(len(title)):
        try:
            write_f.writerow((title[i],company[i],destination[i],money[i],hef[i],information[i]))
        except:
            write_f.writerow((title[i], company[i], destination[i], money[i], hef[i],'######################'))
    file_name.close()
    mail("数据信息写入完成")
def mail(text):
    '''邮件发送'''
    my_sender = 'XXXXX'  # 发件人邮箱账号
    my_pass = 'XXXXX'  # 发件人邮箱授权密码
    my_user = 'XXXXXX'  # 收件人邮箱账号，我这边发送给自己

    try:
        msg=MIMEMultipart()
        content1 = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "爬虫进度"  # 邮件的主题，也可以说是标题
        msg.attach(content1)
        filename = r'bs5_qianchengwuyou.csv'
        if os.path.exists(filename):
            att1 = MIMEApplication(open(filename, 'rb').read())
            att1.add_header('Content-Disposition', 'attachment', filename='data_qcwy.csv')
            msg.attach(att1)
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print("邮件发送失败")

title=[]
company=[]
destination=[]
money=[]
hef=[]
information=[]
start_auto()
