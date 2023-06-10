import smtplib
from email.header import Header
from email.mime.text import MIMEText
from datetime import datetime
from datetime import timedelta
from email.utils import parseaddr, formataddr
import pymysql
from jinja2 import Environment, FileSystemLoader
import os
from pyhtml2pdf import converter
from email.mime.multipart import MIMEMultipart




def pull_news():
    db = pymysql.connect(
        host='db.panel.anyni.com',
        port=13306,
        user='newspaper',
        passwd='JWzXYMKcqDtdS5OL',
        db='newspaper')
    cursor = db.cursor()
    sql = "select date,title_1,content,website,url,keywords from news where date = '" + \
        (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') + "'"
    #print(sql)
    cursor.execute(sql)
    content = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    # print('Insert OK')
    return content


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendmail(msg_content,filename_string):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "notice-mee@qq.com"  # 用户名
    mail_pass = "lvstzjemguyldhig"  # 口令
    sender = 'notice-mee@qq.com'
    receivers = ';'.join(['sunruiqian@139.com','notice-mee@qq.com'])
    # receivers = ['sunruiqian@sd.chinamobile.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # receivers.append(receiver)
    message = MIMEMultipart()
    #message['From'] = Header(f"今日分享文章 {sender}", 'utf-8') 202306腾讯更改政策
    message['From'] = 'NewsHelper <notice-mee@qq.com>'
    message['To'] = Header(f"{receivers}", 'utf-8')
    message['Subject'] = Header('今日分享文章', 'utf-8').encode()
    message.attach(MIMEText(msg_content, 'html', 'utf-8'))


    #message = MIMEText(msg_content, 'html', 'utf-8')
    # message['From'] = Header("notice-mee@qq.com", 'utf-8')
    #message['From'] = _format_addr('今日分享文章 <%s>' % sender)
    # message['To'] =  Header("15063641818@139.com", 'utf-8')
    #message['To'] = ";".join(receivers)
    subject = '今日分享文章 '
    #message['Subject'] = Header('今日分享文章', 'utf-8').encode()

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(f'sendmails/{filename_string}.pdf', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    filename = Header(f"{filename_string}.pdf",'utf-8').encode()
    att1["Content-Disposition"] = f'attachment; filename={filename}'
    message.attach(att1)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
    return


con_lists = pull_news()
print("拉取到"+str(len(con_lists))+"条文章")
content = []
for item in con_lists:
    content.append({'date': str(item[0]),
                    'title': str(item[1]),
                    'content': item[2],
                    'website': item[3],
                    'url': item[4],
                    'keywords':item[5]})
file_loader = FileSystemLoader('../templates')
env = Environment(loader=file_loader)
template = env.get_template('mail.html')
output = template.render(content=content,date=(datetime.now() -timedelta(days=1)).strftime('%Y-%m-%d'))
filename_string='今日分享 - ' + (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
file = open(f'sendmails/{filename_string}.html', mode='w', encoding='utf-8')
file.write(output)
file.close

path = os.path.abspath(f'sendmails/{filename_string}.html')
converter.convert(f'file:///{path}', f'sendmails/{filename_string}.pdf')

sendmail(output,filename_string)