#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: ip_proxy.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-04 06:38:30
#*************************************************************************
import urllib, urllib.request
from bs4 import BeautifulSoup
import random
import time
import sqlite3


def contentlist(url):
    proxylist = ('', )
    proxies = {'': random.choice(proxylist)}
    proxy = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    #user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'
    # user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

    time.sleep(random.randint(0, 10))
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read()
    return content


def soup(url):
    ip_soup = BeautifulSoup(str(contentlist(url)), 'lxml')
    td_soup = ip_soup.find_all('td')
    num = 0
    while num < len(td_soup):
        if num % 8 == 0:
            ip.execute("INSERT INTO IP (IP,PORT) VALUES ('%s','%s')" %
                       (td_soup[num].get_text(), td_soup[num + 1].get_text()))
        else:
            pass
        num += 1


ip = sqlite3.connect('ip.db')
try:
    ip.execute('''CREATE TABLE IP
        (IP   TEXT   ,
         PORT TEXT );''')
except:
    ip.execute("DELETE from IP")
    for i in range(10):
        if i == 0:
            url = 'http://www.kuaidaili.com/'
            soup(url)
        else:
            url = 'http://www.kuaidaili.com/proxylist/' + str(i + 1) + '/'
            soup(url)
    ip.commit()
    ip.close()
