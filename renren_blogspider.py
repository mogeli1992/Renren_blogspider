#!/usr/bin/python
# -*- coding: utf-8 -*-
# auther: wellsleep
# ver: 0.1.160406
# @Python 2.7
# ref: 	crifan 	@ http://www.crifan.com/crifan_released_all/website/python/blogstowordpress/
#		Mio		@ https://github.com/MioYvo/renren_blog_spider
#		null	@ https://github.com/zongxiao/promotion/blob/master/python/interest/renren.py

import os
import sys
import re
import urllib2
import urllib
import cookielib
from bs4 import BeautifulSoup
from tornado.escape import utf8

class Renren(object):

    def __init__(self):
        self.name = self.pwd = self.content = self.domain = self.origURL =  ''
        self.operate = ''#登录进去的操作对象
        self.cj = cookielib.LWPCookieJar()
        try: 
            self.cj.revert('./renren.coockie') 
        except Exception,e:
            print e

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)


    def setinfo(self,username,password,domain,origURL):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password
        self.domain = domain
        self.origURL = origURL

    def login(self):
        '''登录人人网'''
        params = {
            'domain':self.domain,
            'origURL':self.origURL,
            'email':self.name, 
            'password':self.pwd}
        print 'login.......'
        req = urllib2.Request( 
            'http://www.renren.com/PLogin.do',
            urllib.urlencode(params)
        )

        self.file=urllib2.urlopen(req).read()        
        newsfeed = open('news.html','w')
        try:
            newsfeed.write(self.file)
        except Exception, e:
            newsfeed.close()
        self.operate = self.opener.open(req) 
        print type(self.operate)
        print self.operate.geturl()

        if self.operate.geturl(): 
            print 'Logged on successfully!'
            self.cj.save('./renren.coockie')
            self.__viewnewinfo()
        else:
            print 'Logged on error'

    def __viewnewinfo(self):
        '''查看好友的更新状态'''
        self.__caiinfo()


    def __caiinfo(self):
        '''采集信息'''       
        h3patten = re.compile('<article>(.*?)</article>')#匹配范围
        apatten = re.compile('<h3.+>(.+)</h3>:')#匹配作者
        cpatten = re.compile('</a>(.+)\s')#匹配内容  
        content = h3patten.findall(self.file)
        print len(content)   
        infocontent = self.operate.readlines()
        print type(infocontent)
        print 'friend newinfo:' 
        for i in infocontent:
            content = h3patten.findall(i)
            if len(content) != 0:
                for m in content:
                    username = apatten.findall(m)
                    info = cpatten.findall(m)
                    if len(username) !=0:
                        print username[0],'说:',info[0]
                        print '----------------------------------------------'
                    else:
                        continue
						
def save_blog(blog_url):
    print blog_url
    req = urllib2.Request(blog_url)    
    html = urllib2.urlopen(req)    
##    print html
    #html = response.read()  
    # soup = BeautifulSoup(open("/Users/mio/Desktop/r_blog.html"), "html.parser")
    soup = BeautifulSoup(html, "html.parser")
##    print soup

    # 日期
    blog_date = soup.find('span', class_="blogDetail-ownerOther-date")
    blog_date = utf8(blog_date.contents[0])
    print blog_date
    # 标题
    title = soup.find('h2', class_="blogDetail-title")
    title = utf8(title.contents[0])
    title = title.replace("/", "\\")
    print title

    # print soup
    a = soup.find_all("div", class_="blogDetail-content")
    blog_content = a[0]
    filename = blog_date.replace(':','-')
    with open("{}{}.html".format(download_dir, filename), "wb") as fw:
        fw.write("# {}\n".format(title))
        fw.write("> {}\n\n".format(blog_date))
        for i in blog_content:
            try:
                fw.write(str(i))
            except Exception as e:
                print e
                pass

    return get_next(soup)


def get_next(soup):
    # 下一篇
    pre_and_next = soup.find_all(class_="blogDetail-pre")
    #print pre_and_next
    if pre_and_next:
        next_blog_url = pre_and_next[0].findAll('a', href=True)
        print next_blog_url[0]['href']
        if next_blog_url:
            return next_blog_url[0]['href']
    return False

def makelist():
    list_path = 'list.html'
    lp = open(list_path,'w');
    for file in os.listdir(download_dir):
        file_path = os.path.join(download_dir,file)
        if os.path.isfile(file_path)==True:
            f = open(file_path)
            header = f.readline()[0:-1] + f.readline()[0:-1];
##            print header
            href = '<p><a href="' + file + '">' + header + '\n'
            print href
            lp.write(href)
            
ren = Renren()
username = 'xxxx@xxx.com'#你的人人网的帐号
password = 'xxxxxxxx'#你的人人网的密码
domain = 'www.renren.com'#人人网的地址
origURL = 'http://www.renren.com/home'#人人网登录以后的地址
blogURL = 'http://blog.renren.com/blog/xxxxxxxx/xxxxxxxx'
download_dir = "f:/renren_blog/"
ren.setinfo(username,password,domain,origURL)
ren.login()
##req = urllib2.Request(blogURL)    
##response = urllib2.urlopen(req)    
##the_page = response.read()    
##print the_page
url = blogURL
os.mkdir(download_dir)
while True:
    next_url = save_blog(url)
    if next_url:
        url = next_url
    else:
        print 'done'
        break
makelist()
