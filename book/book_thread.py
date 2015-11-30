#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: test.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-31 22:12:52
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import urllib,urllib.request
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
        ips = psycopg2.connect(database="ipdb", \
                                user="postgres", \
                                password="qaz123", \
                                host="127.0.0.1", \
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
    def __init__(self,proxylist):
        self.timeout = 30
        self.sleep = 1
        socket.setdefaulttimeout(self.timeout)
        self.proxylist = proxylist
#        self.proxies = {'https':self.proxylist}
        self.proxies = {'https':random.choice(self.proxylist)}
        print(self.proxylist)
        # self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:42.0) Gecko/20100101 Firefox/42.0'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36'
        self.headers = { 'User-Agent' : self.user_agent, \
                        'Referer':'http://www.douban.com/'}

    def contentlist(self,url):
        time.sleep(5)
        cj = http.cookiejar.CookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        proxy = urllib.request.ProxyHandler(self.proxies)
        # proxy = urllib.request.FancyURLopener(self.proxies)
        opener = urllib.request.build_opener(proxy,cookie_support)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        return content

    def Imglist(self,url):
        proxy = urllib.request.ProxyHandler(self.proxies)
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read()
        return content

    def saveImg(self,url,fileName):
        """存储图片"""
        data = self.Imglist(url)
        path = 'image/'
        fileName = fileName + '.jpg'
        print(u"正在存储封面:  %s"%(fileName))
        f = open(path + fileName, 'wb')
        f.write(data)
        f.close()

    def intro(self,book_href,tag,name):
        intros = str(self.contentlist(book_href))
        soup = BeautifulSoup(intros,'lxml')
        div_soup = soup.find('div',{'id':'info'})
        intro_soup = soup.find_all('div',{'class':'intro'})
        title = div_soup.get_text()
        if len(intro_soup) == 0:
            try:
                book.execute("INSERT INTO BOOKS (tag,name,title)  \
                                VALUES ('%s','%s','%s')"%(tag,name,title))
                conn.commit()
            except:
                conn.rollback()
        if len(intro_soup) == 1:
            content = intro_soup[0].get_text('',strip=True)
            try:
                book.execute("INSERT INTO BOOKS (tag,name,title,content)  \
                                VALUES ('%s','%s','%s','%s')"%(tag,name,title,content))
                conn.commit()
            except:
                conn.rollback()
        if len(intro_soup) >= 2:
            author = intro_soup[1].get_text('',strip=True)
            content = intro_soup[0].get_text('',strip=True)
            try:
                book.execute("INSERT INTO BOOKS (tag,name,title,content,author)  \
                                VALUES ('%s','%s','%s','%s','%s')"%(tag,name,title,content,author))
                conn.commit()
            except:
                conn.rollback()

    def title(self,url,tag):  #书籍目录
        book = str(self.contentlist(url))
        book_soup = BeautifulSoup(book,'lxml')
        book_div_soup = book_soup.find_all('dd')
        title_soup = book_soup.find_all('a',{'class':'title'})
        div_soup = book_soup.find('div',{'id':'content'})
        img_soup = div_soup.find_all('img')
        num = 0
        '''存储书籍封面'''
        # for img in img_soup:
            # url = img.get('src')
            # self.saveImg(url,title_soup[num].get_text())
            # num += 1

        # num = 0
        for div in book_div_soup:
            self.sleep = 0.1
            time.sleep(self.sleep)
            print('sleep time %d'%(self.sleep))
            book_href = div.find('a').get('href') #书籍介绍链接
            name = title_soup[num].get_text('',strip=True)
            print(u"正在爬取书籍: %s"%(name))
            self.intro(book_href,tag,name)
            num += 1

    def nextpage(self,url):  #书籍目录
        time.sleep(5)
        book = str(self.contentlist(url))
        book_soup = BeautifulSoup(book,'lxml')
        title_soup = book_soup.find_all('a',{'class':'title'})
        return len(title_soup)

    def Tag_url(self,url,tag):
        i = 1
        while i < 1000:
            self.sleep = 0.1
            time.sleep(self.sleep)
            print('sleep time %d'%(self.sleep))
            if i == 1:
                urls = url
                self.title(urls,tag)
            else:
                num = (i-1)*15
                urls = url + '?start=' + str(num)
                '''判断是否有下一页'''
                len_page = self.nextpage(urls)
                if len_page == 0:
                    break
                self.title(urls,tag)
            i += 1

    def start(self):
        print('hello')
        threads = []
        url = 'http://book.douban.com/tag/?view=cloud'
        book_content = str(self.contentlist(url))
        soup = BeautifulSoup(book_content,'lxml')
        a_soup = soup.find_all('a',{'class':'tag'})
        for a in a_soup:  #获取节点标签
            url = 'http://www.douban.com/tag/' + urllib.parse.quote(a.get_text('',strip=True)) + '/book'
            print(u"正在爬取节点: %s"%(a.get_text('',strip=True)))
            tag = a.get_text('',strip=True)
    #        self.Tag_url(url,tag)
            t = threading.Thread(target=self.Tag_url,args=(url,tag))
            threads.append(t)
        return threads

if __name__ == '__main__':
    try:
        conn = psycopg2.connect(database="Douban_Book", \
                                user="postgres", \
                                password="qaz123", \
                                host="127.0.0.1", \
                                port="5432")
        print ("Opened database successfully")
        book = conn.cursor()
        # book.execute('''CREATE TABLE BOOKS
                    # (ID  SERIAL PRIMARY KEY,
                    # TAG                 TEXT,
                    # NAME                TEXT,
                    # TITLE               TEXT,
                    # AUTHOR              TEXT,
                    # CONTENT             TEXT);''')
        # print ("Creat database successfully")
        book.execute("DELETE from BOOKS")
        iplist = IP_Proxy()
        spider = Get_DouBan_book(iplist.Proxylist())
        # spider = IP_Proxy()
        # spider.start()
        threads = spider.start()
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        conn.commit()
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
    except socket.error:
        print('time out')
