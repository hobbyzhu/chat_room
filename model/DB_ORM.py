"""
mysqlORM
"""


import time
from common.config import *
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.testing.schema import Table

# 建立于Mysql链接

engine = create_engine('mysql+pymysql://{0}:{1}@{2}/{3}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME), echo=False,
                       pool_size=1000, )

# 定义模型类继承的父类，以及数据链接
DBsession = sessionmaker(bind=engine)
# 继承
dbsession = scoped_session(DBsession)  # 线程安全
Base = declarative_base()
# 定义元数据
md = MetaData(bind=engine)


class Users(Base):
    __table__ = Table('users', md, autoload=True)

    # 通过query 和 filter查询 ，all返回多行数据 first返回一条数据
    # result1 = dbsession.query(Users).all()  # 返回是可遍历的对象
    # result2 = dbsession.query(Users).filter_by(userid=1).all()  # 返回对象是list ,filter_by只能等值查询
    # result3 = dbsession.query(Users).filter(Users.userid = 5).first()  # 返回对象,获取一条数据
    # result4 = dbsession.query(Users.userid, Users.username).filter(Users.userid < 5).first()  # 增加约束条件--》列

    def gat_user(self, username):
        result = dbsession.query(Users).filter_by(user_name=username).first()
        return result


a = Users()
r = a.gat_user('user2')
print(r.__dict__)