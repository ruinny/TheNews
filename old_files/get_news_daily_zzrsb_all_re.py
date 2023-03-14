import pandas as pd
from get_news_model import *

datelist = pd.date_range('2022-3-18', '2022-3-30')


for date in datelist:
    url = 'http://www.zuzhirenshi.com/dianzibao/' + date.strftime('%Y-%m-%d') + '/1/index.htm'
    news=News('组织人事报')
    page_url=news.get_news_pages(url)
    try:
        num=news.insert_db()
    except:
        continue
        print("date.strftime('%Y-%m-%d')"+提取错误)
    del news