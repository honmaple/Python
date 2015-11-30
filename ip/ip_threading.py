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
import urllib,urllib.request
from bs4 import BeautifulSoup
import psycopg2
import random
import threading
import socket

class GetProxy(object):
    def __init__(self):
        self.timeout = 30
        socket.setdefaulttimeout(self.timeout)
        self.proxylist = ('120.195.199.251:80')
        self.proxies = {'':random.choice(self.proxylist)}
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }

    def contentlist(self,url):
        proxy = urllib.request.ProxyHandler(self.proxies)
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

        time.sleep(random.randint(0,5))
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read()
        return content
    def test(self,ip,port):
        try:
            proxy = ip + ':' + port
            proxies = {'http':proxy}
            print(proxies)
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = { 'User-Agent' : user_agent }
            proxy = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
            urllib.request.install_opener(opener)

            url = 'http://www.baidu.com'
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request)
            content = response.read()
            return content
        except urllib.request.URLError as e:
            print(e.reason)
            content = '1'
            return content
        except socket.error:
            print('time out')
            content = '1'
            return content



    def soup(self,url):
        print ("Creat database successfully")
        ip_soup = BeautifulSoup(str(self.contentlist(url)),'lxml')
        td_soup = ip_soup.find_all('td')
        num = 0
        while num < len(td_soup):
            if num%8 == 0 :
                a = td_soup[num].get_text()
                b = td_soup[num+1].get_text()
                test_proxy = self.test(a,b)
                if len(test_proxy) >= 1000:
                    print("%s:%s"%(td_soup[num].get_text(),td_soup[num+1].get_text()))
                    ip.execute("INSERT INTO IPS (IP,PORT) VALUES ('%s','%s')"%(td_soup[num].get_text(),td_soup[num+1].get_text()));
                    conn.commit()
                else:
                    print(u'该IP不能使用')
            else:
                pass
            num += 1
    def run(self,url):
        self.soup(url)

    def start(self):
        """程序入口"""
        threads = []
        for i in range(10):
            if i == 0:
                url = 'http://www.kuaidaili.com/'
                t = threading.Thread(target=self.run,args=(url,))
                threads.append(t)
            else:
                url = 'http://www.kuaidaili.com/proxylist/' + str(i+1) +'/'
                t = threading.Thread(target=self.run,args=(url,))
                threads.append(t)
        return threads


if __name__ == '__main__':
    try:
        conn = psycopg2.connect(database="ipdb", \
                                user="postgres", \
                                password="qaz123", \
                                host="127.0.0.1", \
                                port="5432")
        print ("Opened database successfully")
        ip = conn.cursor()
        # ip.execute('''CREATE TABLE IPS
                # (ID  SERIAL PRIMARY KEY,
                # IP               TEXT  NOT NULL,
                # PORT             TEXT  NOT NULL);''')
        # print ("Creat database successfully")
        ip.execute("DELETE from IPS")
        spider = GetProxy()
        threads = spider.start()
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
    #    conn.commit()
        conn.close()
    except urllib.request.URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        else:
            print("Thank you")
        conn.close()
