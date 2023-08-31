# -*- coding:utf-8 -*-
import pymysql


class DataContext:
    def __init__(self, host, port, user, pwd, db):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db

    def __get_connect(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.db,
                                    charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def __get_connect_as_dic(self):
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd, database=self.db,
                                    charset="utf8")
        cur = self.conn.cursor(pymysql.cursors.DictCursor)
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def exec_query(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        res_list = cur.fetchall()

        # 查询完毕后必须关闭连接
        cur.close()
        self.conn.close()
        return res_list

    def exec_query_as_dict(self, sql):
        cur = self.__get_connect_as_dic()
        cur.execute(sql)
        res_list = cur.fetchall()
        # 查询完毕后必须关闭连接
        cur.close()
        self.conn.close()
        return res_list

    def exec_query_one(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        res_list = cur.fetchone()
        # 查询完毕后必须关闭连接
        cur.close()
        self.conn.close()
        if res_list:
            return res_list[0]
        return None

    def exec_query_one_as_dict(self, sql):
        cur = self.__get_connect_as_dic()
        cur.execute(sql)
        res_list = cur.fetchone()
        # 查询完毕后必须关闭连接
        cur.close()
        self.conn.close()
        if res_list:
            return res_list
        return None

    def exec_non_query(self, sql):
        cur = self.__get_connect()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def exec_many_non_query(self, sql, vals_list):
        cur = self.__get_connect()
        cur.executemany(sql, vals_list)
        self.conn.commit()
        cur.close()
        self.conn.close()

    def exec_many_non_query_rollback(self, sql, vals_list):
        cur = self.__get_connect()
        try:
            cur.executemany(sql, vals_list)
            self.conn.commit()
            cur.close()
            self.conn.close()
        except Exception as e:
            self.conn.rollback()
        finally:
            cur.close()
            self.conn.close()

    def exec_create_table(self, table_name, columns):
        cur = self.__get_connect()
        try:
            create_table_query = f"CREATE TABLE {table_name} ("
            for column in columns:
                create_table_query += f"{column['name']} {column['type']}, "
            create_table_query = create_table_query.rstrip(", ") + ")"
            cur.execute(create_table_query)
            self.conn.commit()
            cur.close()
            self.conn.close()
        except Exception as e:
            self.conn.rollback()
        finally:
            cur.close()
            self.conn.close()

