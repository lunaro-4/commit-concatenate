import sqlalchemy
from sqlalchemy.orm import sessionmaker
import SQL

# engine = sqlalchemy.create_engine("mysql+pymysql://root:root@localhost:3306/app")
engine = sqlalchemy.create_engine("sqlite:///../db.sqlite3")
session = sessionmaker(bind=engine)
connection = session()
new_user = SQL.Users("terere", "aassddff")
connection.add(new_user)
connection.commit()
goods = connection.query(SQL.Users).all()
print(goods)
res = connection.execute(sqlalchemy.text("SELECT * from users"))
print(res.fetchall())
