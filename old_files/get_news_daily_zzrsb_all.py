from datetime import datetime
from datetime import timedelta
import pymysql
from requests_html import HTMLSession
from pymysql.converters import escape_string
from pprint import pprint
import time
import pandas as pd
import jieba.analyse

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
db = pymysql.connect(
    host='db.panel.anyni.com',
    port=13306,
    user='newspaper',
    passwd='JWzXYMKcqDtdS5OL',
    db='newspaper')
cursor = db.cursor()


def get_news_page(news_date):
    # 获取新闻链接
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
    session = HTMLSession()
    url = 'http://www.zuzhirenshi.com/dianzibao/' + news_date + '/1/index.htm'
    pages = session.get(url, headers={'user-agent': ua})
    pages.html.render(timeout=60, sleep=10)
    page = pages.html.find('div#BanMianMuLu', first=True)
    if page:
        urls = page.absolute_links
    else:
        urls = None
    session.close()
    return urls


# def get_news_lists(news_page):
#     # 获取新闻链接
#     ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
#     session = HTMLSession()
#     lists = session.get(news_page, headers={'user-agent': ua})
#     lists.html.render(timeout=20, sleep=10)
#     list = lists.html.find('div#InfoList', first=True)
#     if list is not None:
#         return list.absolute_links

def get_news_lists(url):
    # 获取新闻链接
    session = HTMLSession()
    pages = session.get(url, headers={'user-agent': ua})
    pages.html.render(timeout=60, sleep=10)
    page=pages.html.find('div#InfoList', first=True)
    if page:
        news_links = pages.html.find('div#InfoList', first=True).absolute_links
    else:
        news_links=''
    session.close()
    if news_links:
        return news_links


def get_news(url, date):
    session = HTMLSession()
    pages = session.get(url, headers={'user-agent': ua})
    pages.html.render(timeout=60)
    title_html = pages.html.find('div.listhottitle3', first=True)
    if title_html:
        title = title_html.text
    else:
        title = ''
    content_html = pages.html.find('div.innercontent', first=True)
    if content_html:
        content = content_html.html
        keyword = ','.join(
            jieba.analyse.textrank(pages.html.find('div.innercontent', first=True).text, topK=5))
    else:
        content = ''
        keyword=''
    # date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    website = '组织人事报'
    news = {
        'date': date,
        'title': title,
        'content': content,
        'keyword': keyword,
        'website': website,
        'url': url}
    session.close()
    return news


datelist = pd.date_range('2022-01-18', '2022-06-30')

for date in datelist:
    urls = get_news_page(date.strftime('%Y-%m-%d'))
    if urls:
        for url in urls:
            print(url)
            news_links = get_news_lists(url)
            for link in news_links:
                # print(link)
                news = get_news(link, date)
                time.sleep(6)
                sql = "insert into news (date,title_1,content,keywords,website,url) values ('%s','%s','%s','%s','%s','%s')" % (
                    news['date'], news['title'], escape_string(
                        news['content']), news['keyword'], news['website'],
                    news['url'])
                try:
                    cursor.execute(sql)
                    db.commit()
                    print('插入成功' + link)
                except Exception as e:
                    db.rollback()
                    print("提交错误" + link)
    else:
        print('nothing')


cursor.close()
db.close()
