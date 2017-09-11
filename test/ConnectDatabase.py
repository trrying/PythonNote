import pymysql

# 打开数据库连接
db = pymysql.connect("192.168.1.4","root","12345","spider")

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



data = cursor.fetchone()

print(data)

db.close()
