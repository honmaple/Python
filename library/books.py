#*************************************************************************
#   Copyright © 2015 JiangLin. All rights reserved.
#   File Name: sqlite.py
#   Author:JiangLin
#   Mail:xiyang0807@gmail.com
#   Created Time: 2015-10-26 07:36:41
#*************************************************************************
#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import urllib,urllib.request
from bs4 import BeautifulSoup
import re
import sqlite3

try:

    url = 'http://210.29.99.7:8080/top/top_lend.php'
    # 伪装成浏览器
    user_agent = [{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
            {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
            {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]
    headers = { 'User-Agent' : user_agent }
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    book_content = str(content)
    # 打开数据库
    books = sqlite3.connect('books.db')
    print ("Opened database successfully")
    # 创建数据库，如果数据库以存在则插入数据
    try:
        books.execute('''CREATE TABLE BOOKS
            (ID   INT   NOT NULL,
             BOOKNAME TEXT NOT NULL,
            CONTENT TEXT NOT NULL);''')
    except:
        soup = BeautifulSoup(book_content,"lxml")
        main_soup = soup.find('div',{'id':'mainbox'})
        # 正则匹配cls_no的链接
        main_href = soup.find_all(href=re.compile("cls_no"))
        # num ID数目
        num = 0
        # 删除数据库,本来是更新数据库的，小数据直接删除了
        books.execute("DELETE from BOOKS")
        for href in main_href:
            print(href.get_text())
            url = 'http://210.29.99.7:8080/top/top_lend.php' + href.get('href')
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(url)
            content = response.read().decode('utf-8')
            book_list_content = str(content)
            book_list_soup = BeautifulSoup(book_list_content,"lxml")
            book_list_list = book_list_soup.find_all('a',{'class':'blue'})
            for book1 in book_list_list:
                num += 1
                print(book1.get_text())
                book_list_href = book1.get('href').replace('..','')
                if book_list_href == '/opac/book_cart.php':
                    continue
                elif book_list_href == '/opac/search.php':
                    continue
                elif book_list_href == '/opac/book_cart.php':
                    continue
                else:
                    url = 'http://210.29.99.7:8080' + book_list_href
                    request = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(url)
                    content = response.read().decode('utf-8')
                    book_item_content = str(content)
                    book_item_soup = BeautifulSoup(book_item_content,"lxml")
                    book_item_indro = book_item_soup.find_all('dl',{'class':'booklist'})
                    print('========================================')
                    # 这里太耽搁时间，将CONTENT内容传入数据库
                    ber =0
                    for book in book_item_indro:
                        ber += 1
                    book = ' '
                    for i in range(0,ber):
                        book += book_item_indro[i].get_text() #字符串连接
                    book = book.replace('\n\n','')
                    print(book)
                    books.execute("INSERT INTO BOOKS (ID,BOOKNAME,CONTENT) \
                            VALUES ('%d','《%s》','{%s\n}')"%(num,book1.get_text(),book));

except:
    books.commit()
    books.close()

