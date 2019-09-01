# coding:utf-8

# -*- coding: utf-8 -*-

import pymysql
import logging
import traceback


class DbMysql(object):
    def __init__(self, host, port, user, password, db):
        self.my_host = host
        self.my_port = port
        self.my_user = user
        self.my_password = password
        self.my_db = db
        self.my_conn = None
        self.connect()

    def connect(self):
        try:
            self.my_conn = pymysql.connect(host=self.my_host,
                                           user=self.my_user,
                                           passwd=self.my_password,
                                           port=self.my_port,
                                           db=self.my_db,
                                           charset="utf8")
            logging.info('connect to msyql {0}'.format(self.my_conn))
        except Exception as err:
            logging.error('get_mdb_conn connect error:{0}'.format(err))
            self.my_conn = None

    def execute(self, sqls):
        status_code = 0
        if not isinstance(sqls, list):
            sqls = [sqls]
        with self.my_conn.cursor() as cursor:
            i = 0
            retry = False
            while i < len(sqls):
                sql = sqls[i]
                try:
                    cursor.execute(sql)
                    # logging.info(sql)
                except Exception as e:
                    if e.args[0] == 1062:
                        pass
                    elif e.args[0] == 2006 or e.args[0] == "(0, '')":
                        if not retry:
                            retry = True
                            self.connect()
                            # 重新连接 再次执行
                            continue
                        else:
                            status_code += -1
                    else:
                        logging.error(e)
                        logging.error(sql)
                        logging.error(traceback.format_exc())
                        status_code += -1
                i += 1
                if retry:
                    retry = False
        return status_code

    def query(self, sql):
        rows = []
        with self.my_conn.cursor() as cursor:
            try:
                cursor.execute(sql)
                rows = cursor.fetchall()
            except Exception as e:
                if e.args[0] != '(0, \'\')':
                    logging.error(e)
                    logging.error(sql)
                    logging.error(traceback.format_exc())
        return rows

    def insert(self, open_id, mobile_phone):
        sql="insert into userinfo (open_id, mobile_phone) VALUE (%s,%s);"
        with self.my_conn.cursor() as cursor:
            try:
                cursor.execute(sql, open_id, mobile_phone)
            except Exception as e:
                if e.args[0] != '(0, \'\')':
                    logging.error(e)
                    logging.error(sql)
                    logging.error(traceback.format_exc())

    def commit(self):
        self.my_conn.commit()

    def rollback(self):
        self.my_conn.rollback()

    def close(self):
        self.my_conn.close()
