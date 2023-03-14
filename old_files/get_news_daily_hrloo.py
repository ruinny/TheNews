
from datetime import datetime
from datetime import timedelta
import pymysql
from requests_html import HTMLSession
from pymysql.converters import escape_string
from pprint import pprint
import time
import jieba.analyse


ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
urls = ['https://www.hrloo.com/rz/hot/p1']

db = pymysql.connect(
    host='db.panel.anyni.com',
    port=13306,
    user='newspaper',
    passwd='JWzXYMKcqDtdS5OL',
    db='newspaper')
cursor = db.cursor()


def get_news_lists(url):
    # 获取新闻链接
    news_links = []
    session = HTMLSession()
    pages = session.get(url, headers={'user-agent': ua})
    pages.html.render(timeout=60, sleep=10)
    page = pages.html.find('div.text')
    if page:
        for item in page:
            date = item.find('span.r.gray9.fst', first=True).text
            if (datetime.now() - timedelta(days=1)
                    ).strftime('%Y-%m-%d') == date:
                news_links.append(item.find('h2 a', first=True).attrs['href'])
                # title=item.find('h2 a',first=True).attrs['href']
                # zhaiyao=item.find('p',first=True).text
                # pinglun=item.find('p.mt10.gray9 >span.mr5',first=True).text
    print('三茅人力'+url+'获取到' + str(len(news_links)) + '条')
    session.close()
    return news_links


def get_news(url):

    session = HTMLSession()
    i = 1
    while i <= 5:
        try:
            pages = session.get(url, headers={'user-agent': ua})
            break
        except BaseException:
            time.sleep(5)
            i = i + 1
            continue
    pages.html.render(timeout=60)
    title_html = pages.html.find('h1.rztpl-tit', first=True)
    if title_html:
        title = title_html.text
    else:
        title = ''
    content_html = pages.html.find('div.rztpl-txt.rztpl-txt-def', first=True)
    if content_html:
        content = content_html.html
        keyword = ','.join(
            jieba.analyse.textrank(pages.html.find('div.rztpl-txt.rztpl-txt-def', first=True).text, topK=5))
    else:
        content = ''
        keyword = ''


    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    website = '三茅人力资源网'
    news = {
        'date': date,
        'title': title,
        'content': content,
        'keyword': keyword,
        'website': website,
        'url': url}
    session.close()
    return news


for url in urls:
    news_links = get_news_lists(url)
    if news_links:
        for link in news_links:
            news = get_news(link)
            time.sleep(10)
            sql = "insert into news (date,title_1,content,keywords,website,url) values ('%s','%s','%s','%s','%s','%s')" % (
                news['date'], news['title'], escape_string(news['content']), news['keyword'], news['website'], news['url'])
            try:
                cursor.execute(sql)
                db.commit()
                print('插入成功' + link)
            except Exception as e:
                db.rollback()
                print("提交错误" + link)


cursor.close()
db.close()

#
# def get_today_new():
#     global sql
#     db = pymysql.connect(
#         host='db.panel.anyni.com',
#         port=13306,
#         user='newspaper',
#         passwd='JWzXYMKcqDtdS5OL',
#         db='newspaper')
#     cursor = db.cursor()
#     sql = sql.strip(',') + ';'
#     print(sql)
#     cursor.execute(sql)
#     db.commit()
#     cursor.close()
#     db.close()
#     print('Insert OK')
#
#
# for url in urls:
#     news_links = get_news_lists(url)
#     for link in news_links:
#         get_news(link)
