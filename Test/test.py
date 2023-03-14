from requests_html import HTMLSession
#from old_files import get_news_daily_dachang
import random
from datetime import datetime
from datetime import timedelta
import pymysql
from requests_html import HTMLSession
from pymysql.converters import escape_string
import time
import jieba.analyse
import re
from pprint import pprint
from itertools import chain

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# urls = ['https://www.dachangrenshi.com/cat/1007',
#         'https://www.dachangrenshi.com/cat/1006',
#         'https://www.dachangrenshi.com/cat/1005',
#         'https://www.dachangrenshi.com/cat/1008',
#         'https://www.dachangrenshi.com/cat/1003',
#         'https://www.dachangrenshi.com/cat/1002']
#sql = "insert into news (date,title_1,title_2,title_3,content,keywords,website,url) values "


# 获取新闻链接

session = HTMLSession()
pages = session.get('https://www.hrloo.com/rz/hot/p1', headers={'user-agent': ua})
print(pages.html)










