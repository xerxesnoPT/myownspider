# -*- coding: utf-8 -*-
'''
this py file using for testing anti spider
1.setting random user-agent
2.use proxy ip for spider
该类为反爬虫使用代理ip池跟随机请求头
'''
import requests
import random
from bs4 import BeautifulSoup
import time
from yybao.get_proxyip import Proxyip


class Anti_spider(object):
    def __init__(self):
        self.proxypool = Proxyip().getproxyip()
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

    def choice_header(self):
        return random.choice(self.user_agent_list)

    # 获取请求方法，对外提供返回request 默认重连2次，之后使用代理
    def get_context(self, url, proxy=None, num_retry=2):
        headers = {'User-Agent': self.choice_header()}
        if proxy is None:
            try:
                resp = requests.get(url, headers=headers, timeout=2)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                return resp.text
            except:
                if num_retry > 0:
                    print('链接url失败，2s后重连接,剩', num_retry, '次')
                    time.sleep(2)
                    num_retry = num_retry - 1
                    return self.get_context(url, num_retry=num_retry)
                else:
                    print('尝试使用代理')
                    proxies = random.choice(self.proxypool)
                    return self.get_context(url, proxies)
        else:
            try:
                resp = requests.get(url, headers=headers, proxies=proxy, timeout=2)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                return resp.text
            except:
                if num_retry > 0:
                    print('使用代理连接error,2s后重连,剩', num_retry, '次')
                    time.sleep(2)
                    proxies = random.choice(self.proxypool)
                    print('更换代理为', proxies)
                    num_retry = num_retry - 1
                    return self.get_context(url, proxies, num_retry)
                else:
                    print('连接失败,url可能有误')
                    raise RuntimeError('加了代理也链接失败')

# if __name__ == '__main__':
#     url = 'http://ip.chinz.com/'
#     test = Anti_spider()
#     pro = random.choice(test.proxypool)
#     print(pro)
#     context = test.get_context(url)
# soup = BeautifulSoup(context, 'lxml')
# dd = soup.find_all('dd', attrs={'class': 'fz24'})
# print(dd)
# print(context)
