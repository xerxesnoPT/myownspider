import requests
from bs4 import BeautifulSoup
import os
import time
import re
import pymongo
import datetime
import random
class Voanews_crawl(object):
    def __init__(self):
        db = pymongo.MongoClient()
        self.mongo_news_info = db['news']['info']
        self.mongo_news_urlpage = db['news']['pageurl']
        self.href = ''
        self.title =''
        self.time = ''
        self.user_agent_list = [
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

    def _gethtml(self, url, retry=3):
        try:
            headers={'User-Agent': random.choice(self.user_agent_list)}
            res = requests.get(url,headers=headers)
            res.raise_for_status()
            res.encoding = 'utf8'
            return res.text
        except Exception as e:
            if retry>0:
                time.sleep(4)
                print('连接不稳定，正在重连,剩余%s次,随机ua为%s' %(retry,headers))
                return self._gethtml(url, retry=retry-1)
            else:
                print('连接失败，检查vpn设置')
                print(e)

    def _getsoup(self, url):
        try:
            soup = BeautifulSoup(self._gethtml(url), 'lxml')
            return soup
        except Exception as e:
            print(e)

    def get_div(self,url):
        soup = self._getsoup(url)
        baseurl = 'https://www.voanews.com'
        main_div = soup.find('div', id ='content')
        all_a = main_div.find_all('a', class_='img-wrap')
        for a in all_a:
            text_url = a['href'] if 'http' in a['href'] else baseurl+a['href']
            self.href = text_url
            title = a['title']
            self.title = title.strip()
            if self.mongo_news_info.find_one({'_id': text_url}):
                print('该文章已经解析')
            else:
                self.parse_textpage(text_url)


    def parse_textpage(self,url):
        l = []
        l.append(self.title)
        try:
            soup = self._getsoup(url)
            text_div = soup.find('div', class_="wsw")
            # print(text_div)
            self.time = soup.find('time').get_text()
            self.author =soup.find('div',class_='authors').ul.li.contents[1].string
            for child in text_div.children:
                if child.name == 'p':
                    text = child.get_text()
                    l.append(text+'\n')
                elif child.name == 'div':
                    img_ele = child.find_all('img',limit=1)
                    if img_ele:
                        href = img_ele[0]['src']
                        l.append(href)

            post = {"_id":self.href, "标题":self.title,'作者':self.author,'发布时间':self.time,
                    '内容':l,'入库时间':datetime.datetime.now()}
            self.mongo_news_info.save(post)
            print('已经存入',self.title)
            # print(l)
        except Exception as e:
            print(self.title+'解析div定位失败,该网页可能为视频文章，无法解析')
            print(e)


    def write2word(self, savename, date):
        savename = savename+'.doc'
        with open(savename, 'w') as f:
            f.writelines(date)

# 该方法为爬取a标签层数,根据观察,默认设置为2层.否则会爬取到美国新闻所有年份
    def get_all_link(self, url,level=2):
        soup = self._getsoup(url)
        div = soup.find('div', id="content")
        a_next = div.find_all('a',attrs={'href':re.compile(r'^\/[p,z]\/')})
        if level>0:
            for a in a_next:
                baseurl = 'https://www.voanews.com'
                next_url= baseurl+a['href']
                title = a.get_text()
                if self.mongo_news_urlpage.find_one({"板块地址":next_url}):
                    print('改板块地址已入库，直接爬取即可')
                else:
                    post = {'板块地址':next_url,'板块名称':title}
                    self.mongo_news_urlpage.save(post)
                    print('新板块存入mongo')
                    self.get_all_link(next_url,level=level-1)
        else:
            return


if __name__ == '__main__':
    url = 'https://www.voanews.com/'
    crawl = Voanews_crawl()
    # crawl.parse_textpage('https://www.voanews.com/a/united-arab-emirates-sends-yemeni-terror-suspects-eritrean-prison/3919965.html')
    crawl.get_all_link(url)
    urldata = crawl.mongo_news_urlpage.find()
    for data in urldata:
        url = data['板块地址']
        crawl.get_div(url)



