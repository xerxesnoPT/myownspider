import requests
from bs4 import BeautifulSoup
import pymongo
import datetime
import json
from yybao.antispider import Anti_spider


class YYBao(object):
    def __init__(self):
        mongo_db = pymongo.MongoClient()['yingyongbao']
        self.mongo_collection = mongo_db['appinfo']
        self.title = ''
        self.down_href = ''
        self.version = ''
        self.company = ''

    def _gethtml(self, url):
        try:
            anti_spider = Anti_spider()
            return anti_spider.get_context(url)
        except:
            raise RuntimeError('url解析网页失败')

    def _getSoup(self, url):
        html = self._gethtml(url)
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def spiderdoor(self, url):
        soup = self._getSoup(url)
        baseurl = url[:url.rindex('/') + 1]
        # print(baseurl)
        div_ajax = soup.find_all('div', class_='union-list-toggle')
        for div in div_ajax:
            ajax_url = baseurl+div['data-ajaxurl']
            self.parse_json(ajax_url)
        a_elemts = soup.find_all('a', class_="appName ofh")
        count = 0
        re_count = 0
        for a in a_elemts:
            next_url = baseurl + a['href']
            app_name = a.get_text()
            if self.mongo_collection.find_one({'名字': app_name}):
                re_count +=1
            else:
                count += 1
                self.parse_main_appurl(next_url)
        print('共有%d个app重复存在于mongo中。a标签解析总共存储了%d个app' %(re_count,count))

    def parse_json(self, url):
        json_re = requests.get(url)
        appobj = json.loads(json_re.text)['obj']
        count = 0
        re_count = 0
        if appobj:
            for app in appobj:
                app_name = app['appName']
                app_href = app['apkUrl']
                app_version = app['versionName']
                if self.mongo_collection.find_one({'名字': app_name}):
                    re_count += 1
                else:
                    self.down_href = app_href
                    self.version = app_version
                    self.title = app_name
                    self.company = 'json解析，我也不知道怎么取'
                    post = {'名字': self.title,
                            '版本号': self.version,
                            '开发公司名称': self.company,
                            '下载链接': self.down_href,
                            '存入时间': datetime.datetime.now()}
                    self.mongo_collection.save(post)
                    count += 1
            print('json页面解析有%d个已经存在于mongo ,新增部分总共存入%d' % (re_count, count))



    def parse_main_appurl(self, url):
        soup = self._getSoup(url)
        a_downlink = soup.find('a', class_='det-down-btn')['data-apkurl']
        div_app_infos = soup.find_all('div', class_='det-othinfo-data')
        app_title = soup.find('div', class_='det-name-int').get_text()
        app_version = div_app_infos[0].get_text()
        app_company = div_app_infos[2].get_text()
        # print(a_downlink_elemt, app_title, app_version, app_company)
        self.down_href = a_downlink
        self.version = app_version
        self.title = app_title
        self.company = app_company
        post = {'名字': self.title,
                '版本号': self.version,
                '开发公司名称': self.company,
                '下载链接': self.down_href,
                '存入时间': datetime.datetime.now()}
        if self.title:
            self.mongo_collection.save(post)
            print('appinfo 存入')

    def url_producer(self):
        url = 'http://sj.qq.com/myapp/union.htm?orgame=1&typeId=&page=%d'
        page = input('请输入要爬取的页数(目前好像一共就只有8页）:')
        for i in range(1, int(page)+1):
            new_url = url % i
            yield new_url







if __name__ == '__main__':

    test = YYBao()
    gen = test.url_producer()
    for g in gen:
        print(g)
        test.spiderdoor(g)
