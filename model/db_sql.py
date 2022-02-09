# 建议ORM查询，我的操作熟练度低
from pymysql import connect
from common.config import *


class DB(object):
    def __init__(self):
        """
        连接数据库
        """
        self.con = connect(host=DB_HOST,
                           port=DB_POST,
                           database=DB_NAME,
                           user=DB_USER,
                           password=DB_PASSWORD
                           )
        # 创建游标
        self.cousor = self.con.cursor()

    def close(self):
        """
        释放数据库资源
        :return: None
        """
        self.cousor.close()
        self.con.close()


    def get_user_one(self, sql):
        """
        使用sql语句查询用户信息
        :return:
        """
        # 执行sql语句
        self.cousor.execute(sql)

        # 获取查询结果
        query_result = self.cousor.fetchone()

        # 判断是否是否有结果
        if not query_result:
            return None

        # 获取字段名称
        fileds = [f[0] for f in self.cousor.description]


        # 使用字段和数据合成字典
        return_date = {}

        # 构造数据字典
        for fileds, value in zip(fileds, query_result):
            return_date[fileds] = value
        return return_date



if __name__ == "__main__":
    db = DB()
    data = db.get_user_one("select * from users WHERE user_id ='1'")
    print(data)
    db.close()