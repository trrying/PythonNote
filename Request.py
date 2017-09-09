'''
Created on 2014年4月22日

@author: dev.keke@gmail.com
'''
import urllib.request
import json
import pymysql


# 请求百度网页
# cityResponse = urllib.request.urlopen('https://api.ffan.com/ffan/v3/cities')
#
# cityJson = cityResponse.read().decode('unicode_escape')
#
# cityData = json.loads(cityJson)
#
# print(cityData)

# 打开数据库连接
db = pymysql.connect("192.168.1.4","root","12345","spider")

cursor = db.cursor()

cursor.execute("select count(*) from city_list")

data = cursor.fetchone()

print(data)

db.close()


#
# # 指定编码请求
# # 指定编码请求
# # 指定编码请求
# # 指定编码请求
# with urllib.request.urlopen('https://www.baidu.com') as resu:
#     print(resu.read(300).decode('GBK'))
#
# # 指定编码请求
# f = urllib.request.urlopen('https://www.baidu.com')
# print(f.read(100).decode('utf-8'))
