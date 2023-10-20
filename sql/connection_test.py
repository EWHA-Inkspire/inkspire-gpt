import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

# .env 파일에 설정해 둔 sql pw 받아오기
PW = os.getenv("MYSQL_PW")

db = pymysql.connect(
    host="localhost",
    user="gongryong",
    passwd=PW,
    database="inkspire"
)

cursor = db.cursor()

sql = "select * from member"
cursor.execute(sql)
result = cursor.fetchall()
for row in result:
    print(row)
