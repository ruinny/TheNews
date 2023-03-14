#!/bin/bash
cd /root/News
source ENV-News/bin/activate
python3 get_daily_news.py > /root/News/logs/get_daily_news.log 2>&1 &
#python3 send_daily.py > /root/News/logs/send_daily.log 2>&1 &
deactivate