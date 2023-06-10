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


class News():

    def __init__(self, sitename, get_date):
        db = pymysql.connect(
            host='db.panel.anyni.com',
            port=13306,
            user='newspaper',
            passwd='JWzXYMKcqDtdS5OL',
            db='newspaper')
        cursor = db.cursor()
        sql = "select website_url,page_list_div,list_div,date_div,url_div,title_div,content_div from news_sites where website_name='" + sitename + "'"
        cursor.execute(sql)
        data = cursor.fetchone()
        sql2 = "select newspage from news_newspages where website_name='" + sitename + "'"
        cursor.execute(sql2)
        data2 = cursor.fetchall()
        cursor.close()
        db.close()
        self.sitecons = {
            'website_name': sitename,
            'website_url': data[0],
            'page_list_div': data[1],
            'list_div': data[2],
            'date_div': data[3],
            'url_div': data[4],
            'title_div': data[5],
            'content_div': data[6]
        }
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        self.urls = list(chain.from_iterable(data2))
        self.day_delay = 1
        self.get_date = datetime.strptime(get_date.strftime('%Y-%m-%d'),'%Y-%m-%d')
        #保留到天
        pprint('初始化完成')
        pprint(self.sitecons)
        pprint(self.urls)
        pprint(self.get_date)

    def __del__(self):
        print("示例已经销毁")

    def get_news_pages(self, page_url):
        page_urls = []
        session = HTMLSession()
        i = 1
        while i <= 5:
            # 如果站点有高频访问限制，如果抛出错误，等待5秒，重试5次
            try:
                pages = session.get(page_url, headers={'user-agent': self.ua})
                break
            except BaseException:
                time.sleep(5)
                print("waiting 5 s")
                i = i + 1
                continue
        pages.html.render(timeout=60, sleep=10)
        page = pages.html.find(self.sitecons['page_list_div'], first=True)
        if page:
            self.urls = list(page.absolute_links)
        # 提取到的url赋值给self.urls，作为下一步获取新闻连接的入口
        session.close()
        print("获取到页面连接" + str(self.urls))

    def get_news_lists(self, url, list_div,
                       date_div, url_div):
        # 获取新闻链接
        news_links = []
        session = HTMLSession()
        i = 1
        while i <= 5:
            # 如果站点有高频访问限制，如果抛出错误，等待5秒，重试5次

            try:
                pages = session.get(url, headers={'user-agent': self.ua})
                break
            except BaseException:
                time.sleep(5)
                print("未获取news_lists ,waiting 5 s")
                i = i + 1
                continue
        pages.html.render(timeout=60, sleep=10)
        # 渲染页面
        page = pages.html.find(list_div)
        if page:
            for item in page:
                if date_div:
                    date_str = item.find(date_div, first=True).text
                else:
                    date_str = self.get_date.strftime('%Y-%m-%d')
                #r = r"(.*)((((19|20)\d{2})-(0?[13578]|1[02])-(0?[1-9]|[12]\d|3[01]))|(((19|20)\d{2})-(0?[469]|11)-(0?[1-9]|[12]\d|30))|(((19|20)\d{2})-0?2-(0?[1-9]|1\d|2[0-8]))|((((19|20)([13579][26]|[2468][048]|0[48]))|(2000))-0?2-(0?[1-9]|[12]\d)))$(.*)"
                r = '\d{4}-\d{1,2}-\d{1,2}'
                #date = datetime.strptime(re.match(r, date_str).group(), '%Y-%m-%d')
                date = datetime.strptime(re.findall(r,date_str)[0], '%Y-%m-%d')
                # 正则匹配日期
                # print(datetime.strptime((datetime.now() - timedelta(days=self.day_delay)).strftime('%Y-%m-%d'),'%Y-%m-%d'))
                get_date=datetime.strptime(self.get_date.strftime('%Y-%m-%d'),'%Y-%m-%d')

                if get_date == date:
                    temp_url = item.find(url_div, first=True)
                    if temp_url:
                        news_links.append(
                            str(list(temp_url.absolute_links)[0]))
                    # if 'http' in temp_url:
                    #     output_url = temp_url
                    # else:
                    #     output_url = website_url + temp_url
        # print( url + '获取到' + str(len(news_links)) + '条')
        print("获取到新闻连接" + str(news_links))
        session.close()
        return news_links

    def get_news(self, url, title_div, content_div, website_name):
        session = HTMLSession()
        i = 1
        while i <= 5:
            try:
                pages = session.get(url, headers={'user-agent': self.ua})
                break
            except BaseException:
                time.sleep(5)
                i = i + 1
                continue
        pages.html.render(timeout=60)
        title_html = pages.html.find(title_div, first=True)
        if title_html:
            title = title_html.text
        else:
            title = ''
        content_html = pages.html.find(content_div, first=True)
        if content_html:
            content = content_html.html
            keyword = ','.join(
                jieba.analyse.textrank(pages.html.find(content_div, first=True).text, topK=5))
        else:
            content = ''
            keyword = ''

        date = self.get_date.strftime('%Y-%m-%d')
        news = {
            'date': date,
            'title': title,
            'content': content,
            'keyword': keyword,
            'website': website_name,
            'url': url}
        session.close()
        print("获取到文章" + news['title'])
        return news

    def insert_db(self):
        insert_num = 0
        db = pymysql.connect(
            host='db.panel.anyni.com',
            port=13306,
            user='newspaper',
            passwd='JWzXYMKcqDtdS5OL',
            db='newspaper')
        cursor = db.cursor()

        for url in self.urls:
            print("开始提取" + url)

            news_links = self.get_news_lists(
                url,
                self.sitecons['list_div'],
                self.sitecons['date_div'],
                self.sitecons['url_div'])

            if news_links:

                for link in news_links:
                    print("开始提取" + link)
                    news = self.get_news(
                        link,
                        self.sitecons['title_div'],
                        self.sitecons['content_div'],
                        self.sitecons['website_name'])
                    # get_news(url, title_div, content_div, website_name)
                    time.sleep(random.randint(2, 15))
                    # 随机等待2-15s
                    sql = "insert into news (date,title_1,content,keywords,website,url,insert_date) values ('%s','%s','%s','%s','%s','%s','%s')" % (
                        news['date'], news['title'], escape_string(
                            news['content']), news['keyword'], news['website'],
                        news['url'], datetime.now())
                    sql_check="select * from news where url='"+news['url']+"'"
                    try:
                        cursor.execute(sql_check)
                        if cursor.rowcount>0:
                            print("文章已经入库，跳出循环")
                            continue
                        else:
                            cursor.execute(sql)
                            db.commit()
                            print('插入成功' + link)
                            insert_num = insert_num + 1
                    except Exception as e:
                        db.rollback()
                        print("提交错误" + link)
        cursor.close()
        db.close()
        return insert_num
