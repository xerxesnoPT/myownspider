# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import html2text
import re
import random
import time
import os


base_folder = os.getcwd()


def create_folder(name):
    os.chdir(base_folder)
    os.mkdir(name)
    os.chdir(base_folder+'/'+name)


class myQueue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


def get_html(url, count=3):
    headerslist = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    headers = {'User-Agent': random.choice(headerslist)}
    try:
        r = requests.get(url, headers=headers, timeout=2)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        if count > 0:
            print('链接失败,3s后重连,第', count, '次')
            time.sleep(8)
            count = count -1
            return get_html(url, count=count)
        else:
            print('链接失败')

def get_article(q):
    while not q.isEmpty():
        url = q.dequeue()
        print(url)
        page_num = re.search('\d+', url).group()
        new_folder = '第%s页 下载时间 %s' %(page_num,time.ctime())
        create_folder(new_folder)
        pagehtml = get_html(url)
        soup = BeautifulSoup(pagehtml, 'lxml')
        next_div = soup.find('div', class_='pagination')
        a = next_div.find('a', string='Next Page »')
        if a:
            next_link = a.get('href')
            q.enqueue(next_link)
        try:
            head_divs = soup.find_all('div', class_='post_header')
            for div in head_divs:
                alink = div.find('a')['href']
                write2md(alink)
        except:
            print('wrong')


def get_soup(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    try:
        title = soup.find('div', class_='post_header').text.strip()
        title = title+'.md'
        main_text = soup.find('div', class_='post_excerpt')
        main_text.find('a')

        return title, str(main_text)
    except:
        return None


def write2md(url):
    filename, text = get_soup(url)
    filename = re.sub(r'/', '', filename)
    h = html2text.HTML2Text()
    md_text = h.handle(text)
    pattern = r'-\n'
    p = re.compile(pattern)
    md_text = p.sub('-', md_text)
    with open(filename, 'wt', encoding="UTF-8") as file:
        file.write(md_text)
    print("%s 转换markdown成功" %filename)


if __name__ == '__main__':
    page_num = input("请输入从第几页开始下载")
    q = myQueue()
    baseurl = 'http://cn.openerp.cn/blog/page/%s/' %page_num
    q.enqueue(baseurl)
    get_article(q)



