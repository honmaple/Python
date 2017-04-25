#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: markdown.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-04-16 14:08:16 (CST)
# Last Update:星期二 2017-4-16 16:9:17 (CST)
#          By:
# Description: 自动 wrap markdown 文本中的裸链接，
#              例如：将 `https://www.example.com` 转换成 `[https://www.example.com](https://www.example.com)`
#              抽取 markdown 文本中图片链接
# **************************************************************************
import re


class Regex(object):
    url = re.compile(r'\[(?P<alt>.*?)\][(](?P<href>https?://.+?)[)]')
    # url1 = re.compile(
    #     r'[^@\["(](http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    # )
    url1 = re.compile(
        r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    )
    url2 = re.compile(r'<[^>]+>')
    img = re.compile(r'<img.*?src="(?P<src>.+?)".*?></img>')
    img1 = re.compile(r'!\[(?P<alt>.*?)\][(](?P<src>.+?)[)]')


class Helper(object):
    def __init__(self, text):
        self.text = text
        self.imgs = []

    def wrap_links(self):
        text = self.text
        if Regex.url2.search(text):
            #  去除html标签
            for i in Regex.url2.finditer(text):
                r = i.span()
                length = r[1] - r[0]
                text = Regex.url2.sub('@' * length, text, 1)
        if Regex.url.search(text):
            #  去除markdown标记
            for i in Regex.url.finditer(text):
                r = i.span()
                length = r[1] - r[0]
                text = Regex.url.sub('@' * length, text, 1)
        if Regex.url1.search(text):
            # 找到http链接
            length = len(self.text)
            more = 0
            for i in Regex.url1.finditer(text):
                span = i.span()
                if more:
                    span = (span[0] + more, span[1] + more)
                    more = 0
                href = self.text[span[0]:span[1]]
                lhref = href.lstrip()
                space = len(href) - len(lhref)
                string = '{0}[{1}]({1})'.format(' ' * space, lhref)
                if self.text[span[1]] == '\n':
                    string += '\n'
                self.text = self.text[:span[0]] + string + self.text[span[1] +
                                                                     1:]
                more = len(self.text) - length
        return self.text

    def extract_images(self):
        text = self.text
        if Regex.img1.search(text):
            for i in Regex.img1.finditer(text):
                self.imgs.append(i.group('src'))
        if Regex.img.search(text):
            for i in Regex.img.finditer(text):
                self.imgs.append(i.group('src'))
        return set(self.imgs)


if __name__ == '__main__':
    text = '''
    ![aa](1.png) <img src="https://static.baydn.com/static/img/logo_v4.png"></img> ![](https://static.baydn.com/static/img/logo_v1.png)
    Hello World! There is an image: <img src="https://static.baydn.com/static/img/logo_v1.png"></img>
    and There is a link: https://www.google.com/search?q=Hello
    and There is a good link: [https://www.google.com/search?q=Hello](https://www.google.com/search?q=Hello)
    and There is a video: <video src="https://v.qq.com/xyz.mp4"></video>
    and There is a link: https://www.google.com/search?q=Hello https://www.google.com/search?q=Hello
    '''
    h = Helper(text)
    a = h.wrap_links()
    print(a)
