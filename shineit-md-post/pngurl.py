import os
import re
import urllib.request
from urllib.parse import quote

def main(file):
    l  = []
    for f in file:
        if f.endswith('.md'):
            with open(f, 'r', encoding='utf8') as post:
                main_body = post.read()
                pattern = r'.*?(http://.*\.jpg)\)'
                imglist = re.findall(pattern, main_body)
                if imglist:
                    l.append(imglist)
    return l

def downimg(url,img_name):
    print(url)
    url = quote(url, safe='/:?=')
    print(url)
    r = urllib.request.urlopen(url)
    with open(img_name, 'wb') as img:
        img.write(r.read())

if __name__ == '__main__':
    file = os.listdir(os.getcwd())
    imglist = main(file)
    print(imglist)
    for img in imglist:
        for i in img:
            img_name = i[i.rfind('/')+1:]
            print(i)
            print(img_name)
            downimg(i, img_name)

