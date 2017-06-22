from scarpyexp.xcdaili2mysql.mysql_cont import MysqlConnt
import requests
'''
该模块为对mysql中的ip地址进行是否可用验证，若无法使用，直接删除。进行ip池的清洗
'''
class Waship(object):
    def Wash(self):
        sql_connt = MysqlConnt()
        iplist = sql_connt.getip()
        https_url = 'https://www.baidu.com'
        http_url = 'http://www.baidu.com'
        delte_num = 0
        if iplist:
            for ip in iplist:
                url = http_url if ip['type'].lower()=='http' else https_url
                proxyip = ip['type'].lower()+'://'+ip['ip']+':'+ip['port']
                proxydict = {ip['type'].lower(): proxyip}
                try:
                    res = requests.get(url, timeout=2, proxies=proxydict)
                    res.raise_for_status()
                except:
                    sql_connt.deleteip(ip['id'])
                    delte_num +=1
            print('清洗完毕,%d 个ip无用，已经被删除' %delte_num)

if __name__ == '__main__':
    test = Waship()
    test.Wash()

