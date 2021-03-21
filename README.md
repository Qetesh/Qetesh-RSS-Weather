# RSS-Weather
Weather subscription via rss

默认路径为
http://127.0.0.1:8000/weather/rss.xml?location=北京市

测试基于Reeder

pip3 install django feedgen requests

python3 manage.py migrate

python3 manage.py runserver 127.0.0.1:9000