import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "notice-mee@qq.com"  # 用户名
mail_pass = "lvstzjemguyldhig"  # 口令
sender = 'notice-mee@qq.com'
receivers = ';'.join(
    ['sunruiqian@139.com', 'notice-mee@qq.com'])

# receivers.append(receiver)
message = MIMEMultipart()
message['From'] = 'NewsHelper <notice-mee@qq.com>'
message['To'] = Header(f"{receivers}", 'utf-8')
message['Subject'] = Header('今日分享文章', 'utf-8').encode()
#message.attach(MIMEText(msg_content, 'html', 'utf-8'))
print("Load Content")

# message = MIMEText(msg_content, 'html', 'utf-8')
# message['From'] = Header("notice-mee@qq.com", 'utf-8')
# message['From'] = _format_addr('今日分享文章 <%s>' % sender)
# message['To'] =  Header("15063641818@139.com", 'utf-8')
# message['To'] = ";".join(receivers)
subject = '今日分享文章 '
# message['Subject'] = Header('今日分享文章', 'utf-8').encode()

# 构造附件1，传送当前目录下的 test.txt 文件
# att1 = MIMEText(
#     open(
#         f'sendmails/{filename_string}.pdf',
#         'rb').read(),
#     'base64',
#     'utf-8')
# att1["Content-Type"] = 'application/octet-stream'
# # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
# filename = Header(f"{filename_string}.pdf", 'utf-8').encode()
# att1["Content-Disposition"] = f'attachment; filename={filename}'
# message.attach(att1)
# print("Load Attach")

smtpObj = smtplib.SMTP()
smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
smtpObj.login(mail_user, mail_pass)
smtpObj.sendmail(sender, receivers, message.as_string())
print("Send Email Success！")



