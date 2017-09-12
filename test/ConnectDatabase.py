import pymysql

# 打开数据库连接
db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
cursor = db.cursor()

# cursor.execute("select count(*) from city_list")

# sqlStr = "insert into ffan_poi (fp_p_id, fp_p_name, fp_p_address, fp_city, fp_city_id) VALUES (%d,%s,%s,%s,%d)"
# sqlData = {123456, '广州正佳', '广中中山大道', '广州', 404040}
# cursor.execute(sqlStr, sqlData)


# baseInsertSql = """
# insert into ffan_poi (fp_p_id, fp_p_name, fp_p_address, fp_city, fp_city_id, fp_create_time)
# VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
# """
# insertSql = baseInsertSql % (plaza['id'], plaza['plazaName'], plaza['plazaAddress'], plaza['cityName'], plaza['cityId'], 12321)


# cursor.execute("select COUNT(*) from ffan_poi where fp_p_id = '1100819'")
#
# data = cursor.fetchone()
#
# print(data[0])



select_sql = "select * from ffan_poi"
cursor.execute(select_sql)
sql_result = cursor.fetchall()

f = open("sql_bk.txt", "w", encoding='utf8')
for plaza in sql_result:
    plaza_str = str(plaza) + "\n"
    f.write(plaza_str)
f.close()
db.close()
