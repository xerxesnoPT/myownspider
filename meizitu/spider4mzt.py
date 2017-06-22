#-*- coding: utf-8 -*-
import requests
from lxml import etree
class Meizitu(object):
    def get_html(self,url):
        try:
            resp = requests.get(url,timeout=2)
            resp.raise_for_status()
            resp.encoding='utf-8'
            return resp.text
        except:
            return None

    def parse_urllist(self,url,xpath='//p[@class="url"]/a'):
        html = self.get_html(url)
        if html:
            selector = etree.HTML(html)
            elements = selector.xpath(xpath)             #'//p[@class="url"]/a/@href'
            return elements
        else:
            return None

    def download(self,img_urllist,filename):
        for img_url in img_urllist:
            imgbyte = requests.get(img_url,timeout=2).content




    def parse_img(self,url):
        elements = self.parse_urllist(url)
        if elements:
            for ele in elements:
                next_url = ele.attrib['href']
                print(next_url)
                span_elem = self.parse_urllist(next_url,
                         xpath='//div[@class="pagenavi"]/a/span')
                if span_elem:
                    img_last_index = span_elem[-2].text
                    print(img_last_index)






if __name__ == '__main__':
    test = Meizitu()
    url = 'http://www.mzitu.com/all'
    urls = test.parse_img(url)
    for i in urls:
        # attr = i.attrib
        # print(attr['href']+i.text)
        i

















