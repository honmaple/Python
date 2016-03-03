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
import gc


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
        # self.timeout = 40
        self.sleep = 1
        self.count = 3
        # socket.setdefaulttimeout(self.timeout)
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
        self.sleep = random.randint(0, 5)
        time.sleep(self.sleep)
        cj = http.cookiejar.CookieJar()
        cookie_support = urllib.request.HTTPCookieProcessor(cj)
        proxy = urllib.request.ProxyHandler(self.proxies)
        # proxy = urllib.request.FancyURLopener(self.proxies)
        opener = urllib.request.build_opener(proxy, cookie_support)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        return content

    def Imglist(self, url):
        self.sleep = 10
        time.sleep(self.sleep)
        proxy = urllib.request.ProxyHandler(self.proxies)
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        request = urllib.request.Request(url=url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read()
        return content

    def saveImg(self, url, fileName):
        """存储图片"""
        data = self.Imglist(url)
        path = 'image/'
        fileName = fileName + '.jpg'
        print(u"正在存储封面:  %s" % (fileName))
        f = open(path + fileName, 'wb')
        f.write(data)
        f.close()

    def intro(self, book_href, tag, name):
        '''详细内容页'''
        intros = str(self.contentlist(book_href))
        book_soup = BeautifulSoup(intros, 'lxml')
        info_soup = book_soup.find('div', {'id': 'info'})
        try:
            span_soup = info_soup.contents
        except:
            span_soup = info_soup.children
        '''主要信息'''
        infor = []
        for span in span_soup[5::4]:
            infor.append(span.string)

        '''评分'''
        sore = []
        sore_total_soup = book_soup.find('strong', {'class': 'll rating_num '})
        sore_soup = book_soup.find('div', {'class': 'rating_wrap clearbox'})
        sore_span = sore_soup.find_all('span')

        sore_count = []
        sore_count.append(sore_total_soup.string)

        for s in sore_span[4::2]:
            sore.append(s.string)

        intro_soup = book_soup.find_all('div', {'class': 'intro'})
        if len(intro_soup) == 0:
            try:
                book.execute("INSERT INTO BOOKS (tag,name,\
                            publish_company,publish_time,page,price,isbn,\
                            score,score_5,score_4,score_3,score_2,score_1) \
                            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s',\
                            '%s','%s','%s','%s')" % (tag,
                                                     name,
                                                     infor[0],
                                                     infor[-4],
                                                     infor[-3],
                                                     infor[-2],
                                                     infor[-1],
                                                     sore_count[0],
                                                     sore[0],
                                                     sore[1],
                                                     sore[2],
                                                     sore[3],
                                                     sore[4]))
                conn.commit()
            except:
                conn.rollback()
        if len(intro_soup) == 1:
            content = intro_soup[0].get_text('', strip=True)
            try:
                book.execute("INSERT INTO BOOKS (tag,name,\
                            publish_company,publish_time,page,price,isbn,\
                            score,score_5,score_4,score_3,score_2,score_1,\
                            content) \
                            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s',\
                            '%s','%s','%s','%s','%s')" % (tag,
                                                          name,
                                                          infor[0],
                                                          infor[-4],
                                                          infor[-3],
                                                          infor[-2],
                                                          infor[-1],
                                                          sore_count[0],
                                                          sore[0],
                                                          sore[1],
                                                          sore[2],
                                                          sore[3],
                                                          sore[4],
                                                          content))
                conn.commit()
            except:
                conn.rollback()
        if len(intro_soup) >= 2:
            author_content = intro_soup[1].get_text('', strip=True)
            content = intro_soup[0].get_text('', strip=True)
            try:
                book.execute("INSERT INTO BOOKS (tag,name,\
                            publish_company,publish_time,page,price,isbn,\
                            score,score_5,score_4,score_3,score_2,score_1,\
                            author_content,content) \
                            VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s',\
                            '%s','%s','%s','%s','%s','%s')" % (tag,
                                                               name,
                                                               infor[0],
                                                               infor[-4],
                                                               infor[-3],
                                                               infor[-2],
                                                               infor[-1],
                                                               sore_count[0],
                                                               sore[0],
                                                               sore[1],
                                                               sore[2],
                                                               sore[3],
                                                               sore[4],
                                                               author_content,
                                                               content))
                conn.commit()
            except:
                conn.rollback()

        del infor[:]
        del sore[:]
        del sore_count[:]
        del span_soup[:]
        del intro_soup[:]
        del sore_span[:]
        gc.collect()

    def title(self, url, tag):  # 书籍目录
        book = str(self.contentlist(url))
        book_soup = BeautifulSoup(book, 'lxml')
        book_div_soup = book_soup.find_all('dd')
        title_soup = book_soup.find_all('a', {'class': 'title'})
        div_soup = book_soup.find('div', {'id': 'content'})
        img_soup = div_soup.find_all('img')
        # num = 0
        # '''存储书籍封面'''
        # for img in img_soup:
        # url = img.get('src')
        # self.saveImg(url,title_soup[num].get_text())
        # num += 1

        num = 0
        for div in book_div_soup:
            print('sleep time %d' % (self.sleep))
            book_href = div.find('a').get('href')  # 书籍介绍链接
            name = title_soup[num].get_text('', strip=True)
            print(u"正在下载书籍: %s" % (name))
            self.intro(book_href, tag, name)
            num += 1

        del book_div_soup[:]

    def nextpage(self, url):  # 书籍目录
        book = str(self.contentlist(url))
        book_soup = BeautifulSoup(book, 'lxml')
        title_soup = book_soup.find_all('a', {'class': 'title'})
        return len(title_soup)

    def Tag_url(self, url, tag):
        i = 1
        while i < 1000:
            print('sleep time %d' % (self.sleep))
            if i == 1:
                urls = url
                self.title(urls, tag)
            else:
                num = (i-1)*15
                urls = url + '?start=' + str(num)
                '''判断是否有下一页'''
                len_page = self.nextpage(urls)
                if len_page == 0:
                    break
                self.title(urls, tag)
            i += 1

    def start(self):
        threads = []
        url = 'http://book.douban.com/tag/?view=cloud'
        book_content = str(self.contentlist(url))
        soup = BeautifulSoup(book_content, 'lxml')
        a_soup = soup.find_all('a', {'class': 'tag'})
        for a in a_soup:  # 获取节点标签
            url = 'http://www.douban.com/tag/' + urllib.parse.quote(
                a.get_text('', strip=True)) + '/book'
            print(u"正在爬取节点: %s" % (a.get_text('', strip=True)))
            tag = a.get_text('', strip=True)
    #        self.Tag_url(url,tag)
            t = threading.Thread(target=self.Tag_url, args=(url, tag))
            threads.append(t)
        return threads

if __name__ == '__main__':
    try:
        conn = psycopg2.connect(database="Douban_Book",
                                user="postgres",
                                password="qaz123",
                                host="127.0.0.1",
                                port="5432")
        print("Opened database successfully")
        book = conn.cursor()
        # book.execute('''CREATE TABLE BOOKS
        # (ID  SERIAL PRIMARY KEY,
        # TAG                 TEXT,
        # NAME                TEXT,
        # PUBLISH_COMPANY     TEXT,
        # PUBLISH_TIME        TEXT,
        # PAGE                TEXT,
        # PRICE               TEXT,
        # ISBN                TEXT,
        # SCORE               TEXT,
        # SCORE_5             TEXT,
        # SCORE_4             TEXT,
        # SCORE_3             TEXT,
        # SCORE_2             TEXT,
        # SCORE_1             TEXT,
        # AUTHOR_CONTENT      TEXT,
        # CONTENT             TEXT);''')
        # print ("Creat database successfully")
        book.execute("DELETE from BOOKS")
        iplist = IP_Proxy()
        spider = Get_DouBan_book(iplist.Proxylist())
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
        conn.commit()
        conn.close()
    except socket.error:
        print('time out')
