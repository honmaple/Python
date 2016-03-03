#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: text1.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-11-01 04:25:32
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import time
import urllib
import urllib.request
from bs4 import BeautifulSoup
import psycopg2
import random


class GetProxy(object):

    def __init__(self):
        self.proxylist = ('120.195.199.251:80')
        self.proxies = {'': random.choice(self.proxylist)}
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def contentlist(self, url):
        proxy = urllib.request.ProxyHandler(self.proxies)
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

        time.sleep(random.randint(0, 5))
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read()
        return content

    def soup(self, url, number):
        ip_soup = BeautifulSoup(str(self.contentlist(url)), 'lxml')
        td_soup = ip_soup.find_all('td')
        num = 0
        while num < len(td_soup):
            if num % 8 == 0:
                print(
                    "%s:%s" %
                    (td_soup[num].get_text(),
                     td_soup[
                        num +
                        1].get_text()))
                ip.execute("INSERT INTO IPS (ID,IP,PORT) VALUES ('%d','%s','%s')" % (
                    number, td_soup[num].get_text(), td_soup[num+1].get_text()))
                number += 1
                conn.commit()
            else:
                pass
            num += 1
        return number

    def start(self):
        """程序入口"""
        number = 1
        for i in range(10):
            if i == 0:
                url = 'http://www.kuaidaili.com/'
                number = self.soup(url, number)
            else:
                url = 'http://www.kuaidaili.com/proxylist/' + str(i+1) + '/'
                number = self.soup(url, number)


if __name__ == '__main__':
    conn = psycopg2.connect(database="ipdb",
                            user="postgres",
                            password="qaz123",
                            host="127.0.0.1",
                            port="5432")
    ip = conn.cursor()
    # ip.execute('''CREATE TABLE IPS
    # (IP   TEXT   ,
    # PORT TEXT );''')
    # print ("Creat database successfully")
    ip.execute("DELETE from IPS")
    spider = GetProxy()
    spider.start()
    conn.close()
