from get_news_model import *
from send_daily_model import *

get_date = datetime.now() - timedelta(days=1)
# 加载获取新闻的日期
print("获取新闻的日期已设定为" + get_date.strftime('%Y-%m-%d'))


news = News('三茅人力资源', get_date)
num = news.insert_db()
del news

# news = News('组织人事报',get_date)
# date_today = get_date.strftime('%Y-%m-%d')
# url = f'http://www.zuzhirenshi.com/dianzibao/{date_today}/1/index.htm'
# page_url = news.get_news_pages(url)
# num = news.insert_db()
# del news

# news = News('大厂人事', get_date)
# num = news.insert_db()
# del news
#
# news = News('中国人才网', get_date)
# num = news.insert_db()
# del news


sender=Send()
#提取昨天新闻，生成PDF，发送邮件
