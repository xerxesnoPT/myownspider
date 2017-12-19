import os
import re
filelist = os.listdir(os.getcwd())
for f in filelist:
    if f.endswith('.md'):
        with open(f, 'r+', encoding='utf8') as file:
            old = file.read()
            pattern = r'(https://shineit.gitlab.io/)'
            a = re.findall(pattern, old)
            #a = re.sub(pattern, '', old)
            #with open(os.getcwd()+'/new/'+ f, 'w',encoding='utf8') as newfile:
            #    newfile.write(a)
            #    print(f)
            print(a)

