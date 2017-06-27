# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pymysql
class Proxyip(object):
    ipdicts=[]
    #设置链接参数
    conndict = dict(host='127.0.0.1', user='root',
                    passwd='1234', port=3306, db='proxyip_pool',
                    charset='utf8')
    def __init__(self):
        self.dpcon = pymysql.connect(**self.conndict)

#从数据库中返回可用的iplist
    def getproxyip(self):
        cursor = self.dpcon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'select * from proxyip'
        try:
            cursor.execute(sql)
            iplist = cursor.fetchall()
        except Exception as e:
            print(e)
        for i in iplist:
            ip = i['type'].lower()+'://'+i['ip']+':'+i['port']
            linktype = ip.split(':')[0]
            prodict={linktype:ip.strip()}
            self.ipdicts.append(prodict)
        return self.ipdicts

#测试所用ip是否能正常代理
    def get_html(self):
        iplist = self.getproxyip()
        for ipdict in iplist:
            try:
                re = requests.get('http://ip.chinaz.com/',timeout=2, proxies=ipdict)
                soup=BeautifulSoup(re.text, 'lxml')
                dd = soup.find_all('dd',attrs={'class':'fz24'})
                print(dd[0])
            except:
                continue

# if __name__ == '__main__':
#     test = Proxyip()
#     test.get_html()


