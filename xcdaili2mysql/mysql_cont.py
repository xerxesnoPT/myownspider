import pymysql


class MysqlConnt(object):
    c_args = dict(port=3306,
                  passwd='1234',
                  user='root',
                  host='127.0.0.1',
                  charset='utf8',
                  db='proxyip_pool')

    def __init__(self):
        self.dbconnector = pymysql.Connect(**self.c_args)

    def write2db(self, row_tup):
        cursor = self.dbconnector.cursor()
        sql = 'insert into proxyip (address,ip,type,port)' \
              'values(%s,%s,%s,%s)'
        try:
            cursor.execute(sql, row_tup)
            self.dbconnector.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            self.dbconnector.rollback()
        return

    def deleteip(self, id):
        cursor = self.dbconnector.cursor()
        sql = 'delete from proxyip where id = %s'
        try:
            cursor.execute(sql, id)
            self.dbconnector.commit()
            print('无用ip已删除')
        except Exception as e:
            print(e)
            self.dbconnector.rollback()
        return

    def getip(self):
        cursor = self.dbconnector.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'select * from proxyip'
        try:
            cursor.execute(sql)
            iplist = cursor.fetchall()
        except Exception as e:
            print(e)
        return iplist
