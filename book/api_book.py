#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: test.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-31 22:12:52
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import urllib
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote
# import sys
import threading
import random
import time
import psycopg2
import http.cookiejar
import socket


class IP_Proxy(object):

    def Proxylist(self):
        ips = psycopg2.connect(database="ipdb",
                               user="postgres",
                               password="qaz123",
                               host="127.0.0.1",
                               port="5432")
        ip = ips.cursor()
        ip.execute("SELECT *  from ips")
        rows = ip.fetchall()
        proxies = []
        for row in rows:
            proxy = row[1] + ':' + row[2]
            proxies.append(proxy)
            ips.close()
        return proxies


class Get_DouBan_book(object):

    def __init__(self, proxylist):
        self.timeout = 10
        self.sleep = 1
        socket.setdefaulttimeout(self.timeout)
        self.proxylist = proxylist
        self.proxies = {'http': random.choice(self.proxylist)}
        print(self.proxies)
        self.user_agent = [
            'Mozilla/5.0 (Windows; U; Windows NT 6.1;en-US;rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36']

        self.headers = {'User-Agent': random.choice(self.user_agent),
                        'Referer': 'http://www.douban.com/'}
        print(self.headers)

    def contentlist(self, url):
        #self.sleep = self.sleep + 0.1
        # time.sleep(self.sleep)
        cj = http.cookiejar.CookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        proxy = urllib.request.ProxyHandler(self.proxies)
        opener = urllib.request.build_opener(proxy, cookie_support)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        return content

    def start(self):
        url = 'http://book.douban.com/subject/4913064/?from=tag_all'
        book = str(self.contentlist(url))
        book_soup = BeautifulSoup(book, 'lxml')
        info_soup = book_soup.find('div', {'id': 'info'})
        span_soup = info_soup.contents

        '''主要信息'''
        infor = []
        for span in span_soup[5::4]:
            infor.append(span.string)
            # print('%s'%span.string)
        print(infor)

        '''评分'''
        sore = []
        sore_total_soup = book_soup.find('strong', {'class': 'll rating_num '})
        sore_soup = book_soup.find('div', {'class': 'rating_wrap clearbox'})
        sore_span = sore_soup.find_all('span')

        sore_count = []
        sore_count.append(sore_total_soup.string)
        print(sore_count)

        for s in sore_span[4::2]:
            sore.append(s.string)
        print(sore)

        intro_soup = book_soup.find_all('div', {'class': 'intro'})
        if len(intro_soup) == 0:
            print('介绍: %s' % intro_soup)
        if len(intro_soup) == 1:
            content = intro_soup[0].get_text('', strip=True)
            print('介绍: %s' % content)
        if len(intro_soup) >= 2:
            content = intro_soup[0].get_text('', strip=True)
            author = intro_soup[1].get_text('', strip=True)
            print('介绍: %s' % content)
            print('\n')
            print('作者: %s' % author)

if __name__ == '__main__':
    iplist = IP_Proxy()
    spider = Get_DouBan_book(iplist.Proxylist())
    spider.start()
