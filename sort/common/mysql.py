# -*- coding: utf-8 -*-
"""
 * Created by PyCharm.
 * User: nihuan
 * Date: 18-5-9
 * Time: 下午4:37
 * Desc: MYSQL 操作类
 """
__author__ = 'nihuan'


import pymysql.cursors
from config.dbconfig import dbconfig


class Db:
    dbConn = None

    def __init__(self):
        connect = pymysql.connect(host=dbconfig['DB_HOST'], user=dbconfig['DB_USER'], password=dbconfig['DB_PWD'], db=dbconfig[
            'DB_NAME'], port=dbconfig['DB_PORT'])
        connect.set_charset(dbconfig['DB_CHARSET'])
        self.dbConn = connect.cursor(pymysql.cursors.DictCursor)

    """单条查询方法"""
    def select_one(self, table, params, field, order, group):
        db_field = '*'
        db_order = ''
        db_group = ''
        where = self.db_where(params)
        if field != "":
            db_field = field

        if order != "":
            db_order = ' ORDER BY ' + order

        if group != "":
            db_group = 'GROUP BY ' + group
        sql = "SELECT %s FROM %s %s %s %s" % (db_field, table, where, db_group, db_order)
        try:
            self.dbConn.execute(sql)
            row = self.dbConn.fetchone()
            return row
        except pymysql.DatabaseError:
            print("Error: %s" % (sql,))

    """多条查询方法"""
    def select_all(self, table, params, field, page, size, order, group, having):
        db_field = '*'
        db_order = db_having = db_group = ''
        # db_page = 0
        db_size = 20
        where = self.db_where(params)
        if field != "":
            db_field = field

        if order != "":
            db_order = ' order by ' + order

        if group != "":
            db_group = 'group by ' + group

        if page >= 0 and size > 0:
            # db_page = page
            db_size = size

        if having != "":
            db_having = 'HAVING ' + having
        sql = "SELECT %s FROM %s %s %s %s %s LIMIT %s" % (db_field, table, where, db_having, db_group, db_order, db_size)
        print(sql)
        try:
            self.dbConn.execute(sql)
            result = self.dbConn.fetchall()
            return result
        except pymysql.ProgrammingError:
            print("Error: %s %s" % (pymysql.ProgrammingError, sql))

    """数据总量获取"""
    def get_count(self, table, params, group, having):
        db_group = db_having = ''
        where = self.db_where(params)
        if group != "":
            db_group = 'GROUP BY ' + group
        if having != "":
            db_having = 'HAVING ' + having
        sql = "SELECT count(*) AS count FROM %s %s %s %s" % (table, where, db_group, db_having)
        try:
            self.dbConn.execute(sql)
            result = self.dbConn.rowcount
            return int(result)
        except pymysql.DatabaseError:
            print("Error: %s" % (sql,))

    """查询条件处理"""
    @staticmethod
    def db_where(params):
        where = ''
        if params is not None:
            where += 'WHERE '
            joiner = " AND "
            for par in params:
                if type(params[par]) == list:
                    val = params[par][1]
                    if type(val) != list:
                        val = str(val)
                    where += par + params[par][0] + val + joiner
                else:
                    val = str(params[par])
                    where += par + ' = ' + val + joiner
            where = where[:-len(joiner)]
        return where

    """数据库连接关闭"""
    def db_close(self):
        self.dbConn.close()

