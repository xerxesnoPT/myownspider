import os
import random
mkfilepath = input('输入markdown文件所在文件夹路径：')
img_path = input('输入hugo静态图片所在文件夹路径：')
img_folder = img_path[img_path.rfind('/')+1:]
print(img_folder)

folder = os.listdir(mkfilepath)
print (folder)
imge_list = os.listdir(img_path)

for f in folder:
    if f.endswith('.md'):
        filename = f[:-3]
        print(filename)
        img = random.choice(imge_list)
        data = '''+++\ntitle = "%s"\nauthors = ["Tony Gu"]\n\
categories = ["教程"]\n\
tags = ["Odoo", "Blog"]\n\
date = "2017-10-09"\n\
draft = false\n\
image = "/img/post/%s"
+++''' % (filename, img_folder+'/'+img)
        with open(mkfilepath+'/'+f, 'r+', encoding='utf8') as mdfile:
            old = mdfile.read()
            mdfile.seek(0)
            mdfile.write(data.strip())
            mdfile.write('\n')
            mdfile.write(old)


