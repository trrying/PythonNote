import pymysql

# 打开数据库连接
db = pymysql.connect("192.168.1.4","root","12345","spider")

cursor = db.cursor()

cursor.execute("select count(*) from city_list")

data = cursor.fetchone()

print(data)

db.close()
