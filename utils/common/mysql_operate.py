import pymysql
from utils.common.read_data import SETTINGS
from utils.common.read_data import ConfigReadINI
from utils.common.logger import logger

_data = ConfigReadINI(SETTINGS).get_element("mysql")

DB_CONF_BASE = {
    "host": _data["MYSQL_HOST".lower()],
    "port": int(_data["MYSQL_PORT".lower()]),
    "user": _data["MYSQL_USER".lower()],
    "password": _data["MYSQL_PASSWD".lower()],
    "db": _data["MYSQL_DB".lower()]
}


class MysqlDb(object):

    is_exists = dict()

    def __new__(cls, db_conf: dict=DB_CONF_BASE, *args, **kwargs):
        dh_keys = "_".join([str(key) for key in DB_CONF_BASE.values()])
        _is_exist = cls.__name__ + str(dh_keys)
        if _is_exist in cls.is_exists.keys():
            return cls.is_exists[_is_exist]
        self = super(MysqlDb, cls).__new__(cls)
        self._db_conf_base = DB_CONF_BASE
        self._connect = pymysql.connect(**self._db_conf_base, autocommit=True)
        self._cur = self._connect.cursor(cursor=pymysql.cursors.DictCursor)
        cls.is_exists.update({_is_exist: self})
        return self

    def __delete__(self, instance):
        self._cur.close()
        self._connect.close()

    def select_db(self, sql):
        """查询"""
        self._connect.ping(reconnect=True)
        # 使用 execute() 执行sql
        try:
            test = self._cur.execute(sql)
            print(test)
            # 使用 fetchall() 获取查询结果
            data = self._cur.fetchall()
            return data
        except Exception as e:
            logger.info("查询错误 {}".format(e))
            exit()

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self._connect.ping(reconnect=True)
            # 使用 execute() 执行sql
            self._cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            logger.info("操作MySQL出现错误，错误原因：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()


if __name__ == '__main__':
    cmd = r"select * from md_books;"
    cmd2 = r"select * from md_blogs;"
    db = MysqlDb()
    result = db.select_db(cmd)
    db2 = MysqlDb()
    result2 = db.select_db(cmd2)
    #print(result, "\n", result2)
