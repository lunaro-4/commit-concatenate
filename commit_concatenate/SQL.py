from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Integer, Float, Column, ForeignKey, create_engine

Base = declarative_base()

class Users(Base):
    def __init__(self,uname,pwd):
        self.uname = uname
        self.pwd = pwd


    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    uname = Column(String(50))
    pwd = Column(String)
    github_uname = Column(String(50))
    leetcode_uname = Column(String(50))

class Grids(Base):
    __tablename__ ="grids"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))


engine = create_engine("mysql+pymysql://root:root@localhost:3306/app")


Base.metadata.create_all(engine)