import time
import poplib

host = 'pop3.163.com'

username = 'testformailoo@163.com'
password = 'g1234'

pop = poplib.POP3(host)
pop.set_debuglevel(1)
pop.user(username)
auth = pop.pass_(password)
print(auth)
# if __name__ == '__main__':
#     if auth.split(' ')[0] == '+OK':
#         print (username,password)
