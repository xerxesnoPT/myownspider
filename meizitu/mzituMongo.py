# -*- coding: utf-8 -*-
'''
此为bs4版本,获取网络资源并下载
download to mongodb
'''
import requests
import datetime
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from meizitu.antispider import Anti_spider


class Meizitu(object):
    # 返回html响应内容
    def __init__(self):
        #创建mongodb链接对象
        client = MongoClient()
        db = client['beautyphoto']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_urls = []

    def get_html(self, url):
        # try:
        #     resp = requests.get(url,timeout=2)
        #     resp.raise_for_status()
        #     resp.encoding='utf-8'
        #     return resp.text
        # except:
        #     return None
        conn = Anti_spider()
        html = conn.get_context(url)
        return html

    # 首页入口,返回首页所有对应链接
    def parse_a_elements(self, url):
        html = self.get_html(url)
        if html:
            soup = BeautifulSoup(html, 'lxml')
            # 返回所有a元素
            p_all = soup.find_all('p', class_='url')
            a_all = p_all[1].find_all('a')
            return a_all

    # 用来处理进一步页面分析包含照片的张数,返回最大值,然后调用处理函数进行下载url获取
    def parse_img_url(self, url):
        img_soup = BeautifulSoup(self.get_html(url), 'lxml')
        span_all = img_soup.find('div', class_='pagenavi').find_all('span')
        img_index = span_all[-2].get_text()
        max_index = int(img_index) + 1
        page_num = 0
        for page in range(1, max_index):
            page_num += 1
            page_url = url +'/' +str(page)
            self.img(page_url, max_index, page_num)



    # 用来对每个包含照片的url进行img src 获取,返回包含所有url链接的list
    def img(self, page_url,max_index,page_num):
        html = self.get_html(page_url)
        img_url = BeautifulSoup(html, 'lxml').find('div', class_='main-image').find('img')['src']
        self.img_urls.append(img_url)
        if max_index == page_num+1:
            post = {
                '标题': self.title,
                '主题页面': self.url,
                '图片地址': self.img_urls,
                '获取时间': datetime.datetime.now()
            }
            self.meizitu_collection.save(post)
            print('数据存入成功')
        else:
            self.download(img_url)

    # 下载器,传入img url lsit 进行批量下载
    def download(self, url):
        name = url[-9:]
        print('开始保存', url)
        content = requests.get(url).content
        with open(name, 'ab') as f:
            f.write(content)

    # 标签处理器，把首页获取到的a标签进行href 跟text分离，并存入字典
    def a_handle(self, ele):
        savename = ele.get_text()
        self.create_document(savename.replace('?', '_'))
        self.title = savename
        href = ele['href']
        self.url = href
        if self.meizitu_collection.find_one({'主题页面': href}):
            print('该页面已经爬取过了')
        else:
            self.parse_img_url(href)

    # 构造每个网页对应的标题的文件夹用于存放img
    def create_document(self, filename):
        basepath = 'E://spidertest//meizitu'
        os.chdir(basepath)
        savepath = basepath + '//' + filename
        if not os.path.exists(filename):
            os.mkdir(filename)
        os.chdir(savepath)


if __name__ == '__main__':
    test = Meizitu()
    url = 'http://www.mzitu.com/all/'
    a_all = test.parse_a_elements(url)
    for a in a_all:
        test.a_handle(a)
