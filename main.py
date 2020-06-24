#coding=utf-8
import time
import re
import requests
import datetime
import smtplib

def qingqiu():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
                    (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}     #设置headers信息，模拟成浏览器取访问网站
    req = requests.get('目标网站', headers=headers)   #向网站发起请求，并获取响应对象
    content = req.text   #获取网站源码
    pattern = re.compile('.html(.*?)</a>').findall(content)  #正则化匹配字符，根据网站源码设置
    return pattern  #运行qingqiu()函数，会返回pattern的值

def send_email():
    HOST = 'smtp.163.com'   # 网易邮箱smtp
    PORT = '465'
    fajianren = '***@163.com'   #发送人邮箱
    shoujianren = '***@qq.com'   #收件人邮箱
    title = '更新信息通知'     # 邮件标题
    new_pattern = qingqiu()  #提取网页内容列表
    context = new_pattern[0]  # 邮件内容
    smtp = smtplib.SMTP_SSL(HOST, 465)  # 启用SSL发信, 端口一般是465
    res = smtp.login(user=fajianren, password='*******') # 登录验证，password是邮箱授权码而非密码，需要去网易邮箱手动开启
    print('发送结果：', res)
    msg = '\n'.join(
        ['From: {}'.format(fajianren), 'To: {}'.format(shoujianren), 'Subject: {}'.format(title), '', context])
    smtp.sendmail(from_addr=fajianren, to_addrs=shoujianren, msg=msg.encode('utf-8')) # 发送邮件
    print(context)

def update():
    print('通知系统启动中')
    old_pattern = qingqiu()  #记录原始内容列表
    while True:
        new_pattern = qingqiu()  #记录新内容列表
        if (new_pattern!= old_pattern):  #判断内容列表是否更新
            old_pattern=new_pattern    #原始内容列表改变
            send_email()   #发送邮件
        else:
            now=datetime.datetime.now()
            print(now,"尚无更新")
        time.sleep(300) # 五分钟检测一次

if __name__ == '__main__':
    update()
