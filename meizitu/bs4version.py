# -*- coding: utf-8 -*-
'''
此为bs4版本,获取网络资源并下载
'''
import requests
from bs4 import BeautifulSoup
import os
from meizitu.antispider import Anti_spider


class Meizitu(object):
    # 返回html响应内容
    def __init__(self):
        self.save_href = {}

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
            a_all = soup.find('p', class_='url').find_all('a')
            return a_all

    # 用来处理进一步页面分析包含照片的张数,返回最大值,然后调用处理函数进行下载url获取
    def parse_img_url(self, url):
        img_soup = BeautifulSoup(self.get_html(url), 'lxml')
        span_all = img_soup.find('div', class_='pagenavi').find_all('span')
        img_index = span_all[-2].get_text()
        max_index = int(img_index) + 1
        img_list = self.nexturls(url, max_index)
        img_src_list = self.get_img_urls(img_list)
        return img_src_list

    # 构成imgurl下载页
    def nexturls(self, url, max_index):
        all_img = []
        for i in range(1, max_index):
            img_url = url + '/' + str(i)
            all_img.append(img_url)
        return all_img

    # 用来对每个包含照片的url进行img src 获取,返回包含所有url链接的list
    def get_img_urls(self, all_img):
        img_urls = []
        for url in all_img:
            html = self.get_html(url)
            if html:
                img_url = BeautifulSoup(html, 'lxml').find('div', class_='main-image').find('img')['src']
                img_urls.append(img_url)
        return img_urls

    # 下载器,传入img url lsit 进行批量下载
    def download(self, urls):
        for index, url in enumerate(urls):
            img_url = str(index) + url[-4:]
            with open(img_url, 'ab') as f:
                f.write(requests.get(url).content)
        print('下载完成')

    # 标签处理器，把首页获取到的a标签进行href 跟text分离，并存入字典
    def a_handle(self, elements):
        for ele in elements:
            key = ele.get_text()
            value = ele['href']
            self.save_href[key] = value
        return self.save_href

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
    url = 'hp://www.mzitu.com/all/'
    a_all = test.parse_a_elements(url)
    itemdict = test.a_handle(a_all)
    for key, value in itemdict.items():
        test.create_document(key)
        img_down_list = test.parse_img_url(value)
        test.download(img_down_list)
