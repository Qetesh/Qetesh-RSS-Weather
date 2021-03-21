from django.http import HttpResponse
from django.shortcuts import render
from feedgen.feed import FeedGenerator
import requests
import urllib3
import json
import time
import random
urllib3.disable_warnings()

location = '朝阳区'

def print_hi(location):
    url = "https://apip.weatherdt.com/v2/plugin/data/h5?key=zl6uurOJp7&location=%s&lang=cn" % (location)
    i = 0
    res = requests.get(url)
    data = json.loads(res.text)
    title = ('%s每日天气') % location
    yesterday = int(data['yesterday']['tmp_max']) - int(data['daily_forecast'][i]['tmp_max'])
    temp = '降温' if yesterday > 0 else '升温'
    weather = ('<img style src="https://apip.weatherdt.com/20200701/icon/c/%sd.png" referrerpolicy="no-referrer"><br><br>相较于昨天%s%s<br><br>当前天气%s，温度%s，空气状况%s，%s，%s级<br><br>' % (
        (data['now']['cond_code']),
        (temp),
        (yesterday),
        (data['now']['cond_txt']),
        (data['now']['tmp']),
        (data['air_now_city']['aqi']),
        (data['now']['wind_dir']),
        (data['now']['wind_sc'])))
    while i <= 6:
        weather = weather + (
             '<img style src="https://apip.weatherdt.com/20200701/icon/c/%sd.png" referrerpolicy="no-referrer"><img style src="https://apip.weatherdt.com/20200701/icon/c/%sn.png" referrerpolicy="no-referrer"><br><br>%s白天气%s，晚天气%s，最低温度%s，最高温度%s，%s，%s级<br><br>' % (
                 (data['daily_forecast'][i]['cond_code_d']),
                 (data['daily_forecast'][i]['cond_code_n']),
                 (data['daily_forecast'][i]['date']),
                 (data['daily_forecast'][i]['cond_txt_d']),
                 (data['daily_forecast'][i]['cond_txt_n']),
                 (data['daily_forecast'][i]['tmp_min']),
                 (data['daily_forecast'][i]['tmp_max']),
                 (data['daily_forecast'][i]['wind_dir']),
                 (data['daily_forecast'][i]['wind_sc'])))
        i = i + 1
    fg = FeedGenerator()
    fg.id('https://rsshub.qetesh.io/weather/rss.xml')
    fg.title(title)
    fg.description(title)
    fg.link(href='https://rsshub.qetesh.io/weather/rss.xml')
    # fg.author({'name': 'Qetesh', 'email': 'hxk@outlook.com'})
    # fg.logo('')
    # fg.subtitle('This is a cool feed!')

    fe = fg.add_entry()
    fe.id("https://apip.weatherdt.com/v2/h5.html?bg=1&md=02345&lc=%s&key=lmLyU3atUj&%s" %((location), (random.randint(0,99999999))))
    fe.title('%s天气(%s)' % ((location),(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))))
    fe.link(href='https://rsshub.qetesh.io/weather/rss.xml', rel='self')
    # fe.content("123")
    fe.description(weather)

    # while i <= 6:
    #     # print(key, value)
    #     fe = fg.add_entry()
    #     fe.id("https://apip.weatherdt.com/v2/h5.html?bg=1&md=02345&lc=auto&key=lmLyU3atUj&%s" % (random.randint(0,99999999)))
    #     fe.title('%s更新-%s %s 天气' % ((time.strftime("%H:%M", time.localtime())), (location), (data['daily_forecast'][i]['date'])))
    #     # fe.link(href='https://rsshub.qetesh.io/weather/rss.xml', rel='self')
    #     # fe.content("123")
    #     # print((data['daily_forecast'][i]['date']))
    #     fe.description(
    #         '<img style src="https://apip.weatherdt.com/20200701/icon/c/%sd.png" referrerpolicy="no-referrer"><br><br>白天气%s，最低温度%s，最高温度%s<br><br><img style src="https://apip.weatherdt.com/20200701/icon/c/%sn.png" referrerpolicy="no-referrer"><br><br>晚天气%s，最低温度%s，最高温度%s<br><br>' % (
    #             (data['daily_forecast'][i]['cond_code_d']), (data['daily_forecast'][i]['cond_txt_d']),
    #             (data['daily_forecast'][i]['tmp_min']), (data['daily_forecast'][i]['tmp_max']), (data['daily_forecast'][i]['cond_code_n']), (data['daily_forecast'][i]['cond_txt_n']),
    #             (data['daily_forecast'][i]['tmp_min']), (data['daily_forecast'][i]['tmp_max'])))
    #     i = i + 1

    fg.rss_file('RSS-Weather/templates/rss.xml', pretty=True)
    # rssfeed = fg.rss_str(pretty=True)

def rss(request):
    request.encoding = 'utf-8'
    if 'location' in request.GET and request.GET['location']:
        print_hi(request.GET['location'])
    else:
        print_hi("北京市")
    return render(request, "rss.xml", content_type="application/xml")