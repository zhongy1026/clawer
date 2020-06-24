用python实现简单的网站信息更新自动通知
==== 
因为需要及时收到学校研究生网站的消息，每过一小段时间去网站看耗费精力，且不一定能及时的收到消息，所以萌生了用程序定时检测网站是否更新的想法。

实现功能
------- 
检测目标网站更新，获取更新并以邮件形式通知。

适用场景
-------
    票务网站活动更新通知
    学校教务网站更新通知
    新剧新番更新通知
    查成绩通知
    通过程序发邮件，节约登录时间
    
语言
-------
`python3` 开发编译器:`pycharm`

设计思路
-------
爬取网站推送的信息作为预存信息参考-->每隔5分钟爬取一次信息，与数据库预存信息进行比对-->不一样则调用发送邮件函数，否则继续检测。

![liucheng](https://github.com/zhongy1026/-/blob/master/images/liucheng.png)

代码实现
-------
1 调用数据库 
Time、re、requests、datetime、smtplib
Time实现每隔固定时间检测信息是否更新
Re 基于正则表达式匹配字符串，提取出信息列表
Datetime 输出当前时间
Smtplib 发送邮件

2 提取信息列表
                def qingqiu():
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 \
                            (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}     #设置headers信息，模拟成浏览器取访问网站
                    req = requests.get('目标网站网址', headers=headers)   #向网站发起请求，并获取响应对象
                    content = req.text   #获取网站源码
                    pattern = re.compile('.html(.*?)</a>').findall(content)  #正则化匹配字符，根据网站源码设置
                    return pattern  #运行qingqiu()函数，会返回pattern的值

3 更新检测
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

4 发送邮件
        def send_email():
            HOST = 'smtp.163.com'   # 网易邮箱smtp
            PORT = '465'
            fajianren = '*****@163.com' #发件人邮箱
            shoujianren = '******@qq.com'   #收件人邮箱
            title = '信息内容'     # 邮件标题
            new_pattern = qingqiu()  #提取网页内容列表
            context = new_pattern[0]  # 邮件内容
            smtp = smtplib.SMTP_SSL(HOST, 465)  # 启用SSL发信, 端口一般是465
            res = smtp.login(user=fajianren, password='******') # 登录验证，password是邮箱授权码而非密码，需要去网易邮箱手动开启
            print('发送结果：', res)
            msg = '\n'.join(
                ['From: {}'.format(fajianren), 'To: {}'.format(shoujianren), 'Subject: {}'.format(title), '', context])
            smtp.sendmail(from_addr=fajianren, to_addrs=shoujianren, msg=msg.encode('utf-8')) # 发送邮件
            print(context)

运行说明
---
* 使用前需先在send_email函数中设置邮箱账户信息（需获取授权码）
* 需在qingqiu函数中设置目标网站网址
* [获取网易邮箱授权码说明](http://help.mail.163.com/faqDetail.do?code=d7a5dc8471cd0c0e8b4b8f4f8e49998b374173cfe9171305fa1ce630d7f67ac2cda80145a1742516)、[获取QQ邮箱授权码说明](https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=1001256)
