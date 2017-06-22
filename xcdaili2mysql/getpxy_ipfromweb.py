import requests
from bs4 import BeautifulSoup
import random
from scarpyexp.xcdaili2mysql.mysql_cont import MysqlConnt
'''
对xici代理进行代理ip爬取，调用mysql_cont模块把代理ip传入mysql中创建ip池
'''


class ProxyIPSpider(object):
    def __init__(self, url):
        self.url = url

    def _getHtml(self, url):
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
            resp = requests.get(url, headers=headers, timeout=2)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            return resp.text
        except:
            return None

    def getSoup(self, url):
        html = self._getHtml(url)
        item =[]
        if html:
            soup = BeautifulSoup(html, 'lxml')
            tr_eles = soup.find_all('tr', class_='odd')
            for tr in tr_eles:
                tdlis = tr.find_all('td')
                address = tdlis[3].get_text().strip()
                ip = tdlis[1].get_text()
                port = tdlis[2].get_text()
                type = tdlis[5].get_text()
                item.append((address,ip, type, port))
        return item
    #构造nextpage url 发现为nn/1 这里直接使用int构造，通过yield变为生成器，可直接生成nexturl
    def next_page(self, page):
        for i in range(1, page+1):
            nexturl = self.url + '/'+str(i)
            yield nexturl

    #把getSoup方法中爬取到的iplist 储存到本地mysql中
    def write2sql(self, url):
        item = self.getSoup(url)
        connt = MysqlConnt()
        if item:
            for tup in item:
                connt.write2db(tup)
            print('当前页面数据全部存入mysql完毕')


if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn'
    test = ProxyIPSpider(url)
    page = input('要爬取的代理页数：')
    ur = test.next_page(int(page))
    for i in ur:
        a = test.getSoup(i)
        test.write2sql(i)
        # print(i)
