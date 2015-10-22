#!/usr/bin/env python
# -*- coding=UTF-8 -*-
#*************************************************************************
#   File Name: ds.py
#   Author:JiangLin
#   Mail:xiyang0807@163.com
#   Created Time: 2015年10月19日 星期一 00时27分41秒
#*************************************************************************
import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import sys


class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #删除span标签
    removeSpan = re.compile('<Span.*?>|</span>')
    #把换行的标签换为\n
    # replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    # 将空格&nbsp转化为
    replaceSpace = re.compile('&nbsp;')
    #删除& quo字符
    replaceQuo = re.compile('&.*?quo')
    # 将font开头加空格
    # replacePara = re.compile('<font.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>|<br><br><br>|<br><br><br><br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.removeSpan,"",x)
     #   x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replaceSpace,"",x)
        x = re.sub(self.replaceQuo,"",x)
     #   x = re.sub(self.replacePara,"",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class Novel:
    def __init__(self):
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.tool = Tool()
    def getPage(self,url):
        try:
            # url = 'http://202.119.112.75/s/2001/t/2016/p/5/i/' + str(pageIndex) + '/list.htm'
            url = 'http://tieba.baidu.com' + url + '?see_lz=1'
            #构建请求的request
            request = urllib.request.Request(url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib.request.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>',re.S)
            items = re.findall(pattern,pageCode)
            for item in items:
                sys.stdout.write(self.tool.replace(item))
                sys.stdout.flush()
                print('\n')
               # print self.tool.replace(item),
            pattern = re.compile('<div id="post_content.*?>(.*?)</div>',re.S)
            items = re.findall(pattern,pageCode)
            for item in items:
                sys.stdout.write(self.tool.replace(item))
                sys.stdout.flush()
                print('')
                # print self.tool.replace(item),
                return
        except urllib.request.URLError as e:
            if hasattr(e,"reason"):
                print(u"连接baidu失败,错误原因",e.reason)
                return None
    def getPage1(self,url):
        url = 'http://tieba.baidu.com' + url + '?see_lz=1'
        request = urllib.request.Request(url, headers=self.headers)
        response = urllib.request.urlopen(url)
        content = response.read().decode("utf-8")
        soup = BeautifulSoup(content,"lxml")
        div_soup = soup.find_all("div",{'class':'novel-post-content'})
        for td in div_soup:
            print(td.get_text('\n    ','<br/><br/>'))

    def getChioce(self,url):
        #构建请求的request
        url = url
        request = urllib.request.Request(url,headers = self.headers)
        #利用urlopen获取页面代码
        response = urllib.request.urlopen(request)
        pattern = re.compile('<ul id="thread_top_list.*?>(.*?)<i class="icon-top.*?>(.*?)<a href=\"(.*?)\".*?>(.*?)</ul>',re.S)
        # pattern = re.compile('<div class="novel-post-content">(.*?)</div>',re.S)
        #将页面转化为UTF-8编码
        content = response.read().decode('utf-8')
        items = re.findall(pattern,content)
        for item in items:
            # return item[2]
            self.getPage(item[2])

    def getChioce1(self,url):

        request = urllib.request.Request(url,headers = self.headers)
        #利用urlopen获取页面代码
        response = urllib.request.urlopen(request)
        pattern = re.compile('<ul id="thread_top_list.*?>(.*?)<i class="icon-top.*?>(.*?)<a href=\"(.*?)\".*?>(.*?)</ul>',re.S)
        # pattern = re.compile('<div class="novel-post-content">(.*?)</div>',re.S)
        #将页面转化为UTF-8编码
        content = response.read().decode('utf-8')
        items = re.findall(pattern,content)
        for item in items:
            # return item[2]
            self.getPage1(item[2])


    #开始方法
    def start(self):
        print(u"请输入:")
        print(u"1.完美世界  2.我欲封天 3.天火大道 4.九阳踏天  5.戮仙")
        input1 = input()
        if input1 == '1':
            url = 'http://tieba.baidu.com/f?kw=%CD%EA%C3%C0%CA%C0%BD%E7%D0%A1%CB%B5&fr=ala0&loc=rec'
            self.getChioce(url)
        elif input1 == '2':
            url = 'http://tieba.baidu.com/f?kw=%CE%D2%D3%FB%B7%E2%CC%EC&fr=ala0&loc=rec'
            self.getChioce(url)
        elif input1 == '3':
            url = 'http://tieba.baidu.com/f?kw=%CC%EC%BB%F0%B4%F3%B5%C0&fr=ala0&loc=rec'
            self.getChioce(url)
        elif input1 == '4':
            url = 'http://tieba.baidu.com/f?kw=%BE%C5%D1%F4%CC%A4%CC%EC&fr=ala0&loc=rec'
            self.getChioce1(url)
        else:
            url = 'http://tieba.baidu.com/f?kw=%C2%BE%CF%C9&fr=ala0&loc=rec'
            self.getChioce1(url)


spider = Novel()
spider.start()



# url = 'http://tieba.baidu.com/f?kw=%CE%D2%D3%FB%B7%E2%CC%EC&fr=ala0&loc=rec'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = { 'User-Agent' : user_agent }
# try:
    # request = urllib2.Request(url,headers = headers)
    # response = urllib2.urlopen(request)
    # content = response.read().decode('utf-8')
    # pattern = re.compile('<ul id="thread_top_list.*?>(.*?)<i class="icon-top.*?>(.*?)<a href=\"(.*?)\".*?>(.*?)</ul>',re.S)
    # items = re.findall(pattern,content)
    # for item in items:
        # return item[2]
# except urllib2.URLError, e:
    # if hasattr(e,"code"):
        # print e.code
    # if hasattr(e,"reason"):
        # print e.reason
