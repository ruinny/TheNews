import jieba.analyse
from datetime import datetime
from datetime import timedelta
import pymysql
from requests_html import HTMLSession
from pymysql.converters import escape_string
from pprint import pprint
import time

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'


def get_news(url):
    session = HTMLSession()
    pages = session.get(url, headers={'user-agent': ua})
    pages.html.render(timeout=60)
    title = pages.html.find('div.listhottitle3', first=True).text
    content = pages.html.find('div.innercontent', first=True).html
    date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    keyword = pages.html.find('div.innercontent', first=True).text
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


news = get_news(
    'http://www.zuzhirenshi.com/dianzibao/2023-02-21/2/49536450-8596-4d0d-b913-f5e0c5eea5db.htm')

#keywords = jieba.analyse.extract_tags(news['keyword'], topK=5)
keywords = ','.join(jieba.analyse.textrank(news['keyword'], topK=5))

print(news['keyword'])
print()

