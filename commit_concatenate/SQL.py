# from sqlalchemy.orm import declarative_base
# from sqlalchemy import String, Integer, Column, ForeignKey
# import sqlalchemy
#
# Base = declarative_base()
#
#
# class Users(Base):
#     def __init__(self, uname, pwd):
#         self.uname = uname
#         self.pwd = pwd
#
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     uname = Column(String(50))
#     pwd = Column(String(50))
#     github_uname = Column(String(50))
#     leetcode_uname = Column(String(50))
#
#
# class Grids(Base):
#     __tablename__ = "grids"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#
#
# # engine = create_engine("mysql+pymysql://root:root@localhost:3306/app")
# engine = sqlalchemy.create_engine("sqlite:///db.sqlite3")
#
#
# Base.metadata.create_all(engine)
