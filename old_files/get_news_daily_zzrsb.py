from datetime import datetime
from datetime import timedelta
import pymysql
from requests_html import HTMLSession
from pymysql.converters import escape_string
from pprint import pprint
import time
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
    session.close()
    if page:
        return page.absolute_links


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
    news_links = pages.html.find('div#InfoList', first=True).absolute_links
    session.close()
    if news_links:
        return news_links
        print('组织人事报' + url + '获取到' + str(len(news_links)) + '条')


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
        keyword = ''
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    keyword = ','.join(jieba.analyse.textrank(pages.html.find('div.innercontent', first=True).text, topK=5))
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


urls = get_news_page((datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
if urls:
    for url in urls:
        news_links = get_news_lists(url)
        if news_links:
            for link in news_links:
                #print(link)
                news = get_news(link)
                time.sleep(6)
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


def get_older_new(days):
    for i in range(1, days):
        yesterday = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        pages = get_news_page(yesterday)
        page_count = 0
        news_count = 0
        if pages:
            for page in pages:
                pprint('page:' + str(page_count) + page)
                page_count = page_count + 1
                if page:
                    news_list = get_news_lists(page)
                    if news_list:
                        for url in news_list:
                            pprint('news:' + str(news_count) + url)
                            news_count = news_count + 1
                            if url:
                                sql_var = get_news(url)
                                # pprint(sql_var)
                                result = insert_db(sql_var)
                                print(result)



