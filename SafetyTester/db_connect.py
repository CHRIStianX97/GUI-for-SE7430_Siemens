# @Date    : 2019-06-05
# @Author  : James(Jiaxing) Yang
# @File	   : db_connect.py
# @Version : $0.2$

import sys
import pymssql
import os
import pandas as pd
import pprint as pp
import numpy as np


#establish a connection to the db
class database:
    def __init__(self, server, user, pwd, db):
        self.server = server
        self.user = user
        self.pwd = pwd
        self.db = db

    def db_connect(self):
        if not self.db:
            raise Exception(NameError, "没有设置数据库信息")
        self.conn = pymssql.connect(self.server, user=self.user, password=self.pwd, database=self.db,charset="gbk")
        #, charset="utf8"
        cur = self.conn.cursor()
        if not cur:
            raise Exception(NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段

        """
        cur = self.db_connect()
        cur.execute(sql)
        resList = cur.fetchall()
        return resList


    def commit_change(self,sql):
        cur = self.db_connect()
        cur.execute(sql)
        self.conn.commit()


    def close(self):
        self.conn.close()


    def get_info(self):
        DB1 = database(self.server,self.user,self.pwd,self.db)
        DB1.db_connect()
        dr = pd.read_sql('SELECT * from Product', con=DB1.conn)
        self.dr = dr



if __name__ == "__main__":
    pass