from get_news_model import *

url=['https://www.hrloo.com/rz/hot/p1', 'https://www.hrloo.com/rz/hot/p2']

news = News('三茅人力资源')

news.get_news_lists('https://www.hrloo.com/rz/hot/p2','div.text','span.r.gray9.fst','h2 a')