import urllib.request
import json
import pymysql
import time
import sys

baseUrl = "https://api.ffan.com/ffan/v1/city/locationSeek?cityId=%s&size=%s&page=%s"
size = "50"
page = "1"

cityId = "440100"

url = baseUrl % (cityId, size, page)

# print("url = " + url)

plazaResultResponse = urllib.request.urlopen(url)
plazaResultJsonStr = plazaResultResponse.read().decode('utf-8')
plazaResult = json.loads(plazaResultJsonStr)
print("plazaResult : ")
print(plazaResult)
plazaData = plazaResult['data']
print("plazaData : ")
print(plazaData)
plazaList = plazaData['list']
print("plazaList : ")
print(plazaList)

# 打开数据库连接
db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
cursor = db.cursor()

baseInsertSql = """
insert into ffan_poi (fp_p_id, fp_p_name, fp_p_address, fp_city, fp_city_id, fp_create_time)
VALUES ('%d', '%s', '%s', '%s', '%d', '%d')
"""

for plaza in plazaList:
    try:
        insertSql = baseInsertSql % (int(plaza['id']), plaza['plazaName'], plaza['plazaAddress'], plaza['cityName'], int(plaza['cityId']), int(time.time()))
        cursor.execute(insertSql)
        db.commit()
        print("insert sussess " + plaza['plazaName'])
    except:
        db.rollback()
        print("insert fail " + plaza['plazaName'], sys.exc_info())

db.close()






























# 循环获取列表
# more = 1
# while more >= 1
# `fn_id` bigint(20) NOT NULL AUTO_INCREMENT,
#   `fn_title` varchar(100) NOT NULL COMMENT '飞凡新闻的标题',
#   `fn_description` text COMMENT '飞凡新闻的描述',
#   `fn_subtitle` varchar(100) DEFAULT NULL COMMENT '飞凡新闻的子标题',
#   `fn_logo` text NOT NULL COMMENT '飞凡新闻的LOGO',
#   `fn_start_time` bigint(13) NOT NULL DEFAULT '0' COMMENT '飞凡新闻的开始时间',
#   `fn_end_time` bigint(13) NOT NULL COMMENT '飞凡新闻的结束时间',
#   `fn_aid` bigint(20) NOT NULL COMMENT '飞凡自己的新闻ID',
#   `fp_p_id` bigint(20) NOT NULL COMMENT '飞凡自己的场景ID',
#   `fn_create_time` bigint(13) NOT NULL DEFAULT '0' COMMENT '创建时间',
#   `fn_operate_time` bigint(13) NOT NULL DEFAULT '0' COMMENT '处理时间',
#   `fn_apply_sotre` text COMMENT '飞凡适用门店JSON格式:{name:''门店名称'',addre
# baseInsertSql = """
# insert into ffan_poi (fn_id, fn_title, fn_description, fn_subtitle, fn_logo, fn_start_time, fn_end_time, fn_aid, fp_p_id, fn_create_time, fn_operate_time, fn_apply_sotre )
# VALUE ('%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
# """
