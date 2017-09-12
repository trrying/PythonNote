import urllib.request
import json
import pymysql
import time
import sys

def get_plaza():
    city_list = get_city_list()

    print("cityList.len : " + str(len(city_list)))

    base_url = "https://api.ffan.com/ffan/v1/city/locationSeek?cityId=%s&size=%s&page=%s"
    size = 50

    # 打开数据库连接
    db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    cursor = db.cursor()
    baseInsertSql = """
    insert into ffan_poi (fp_p_id, fp_p_name, fp_p_address, fp_city, fp_city_id, fp_create_time)
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
    """

    base_count_sql = "select count(*) from ffan_poi where fp_p_id = '%s'"

    base_update_sql = "update ffan_poi set fp_p_name='%s', fp_p_address='%s', fp_city='%s', fp_city_id='%s', fp_update_time='%s' WHERE fp_p_id = '%s'"

    for city in city_list:
        try:
            page = 1
            city_id = city['cityId']
            while True:
                url = base_url % (city_id, str(size), str(page))
                plaza_result_response = urllib.request.urlopen(url)
                plaza_result_json_str = plaza_result_response.read().decode('utf-8')
                plaza_result = json.loads(plaza_result_json_str)
                plaza_data = plaza_result['data']
                plaza_list = plaza_data['list']
                insert_count = 0
                update_count = 0
                for plaza in plaza_list:
                    try:
                        select_sql = base_count_sql % (plaza['id'])
                        cursor.execute(select_sql)
                        count_plaza = cursor.fetchone()
                        if count_plaza[0] > 0:
                            update_sql = base_update_sql % (plaza['plazaName'], plaza['plazaAddress'], plaza['cityName'], plaza['cityId'], get_current_time(), plaza['id'])
                            update_count += cursor.execute(update_sql)
                        else:
                            insert_sql = baseInsertSql % (plaza['id'], plaza['plazaName'], plaza['plazaAddress'], plaza['cityName'], plaza['cityId'], get_current_time())
                            insert_count += cursor.execute(insert_sql)
                        db.commit()
                    except:
                        db.rollback()
                        print("execute sql fail " + plaza['cityName'] + " " + plaza['plazaName'], sys.exc_info())
                print("insert city : %s  len : %d  insertCount : %d  updateCount : %d  total : %s  page : %d"
                      % (city['cityName'], len(plaza_list), insert_count, update_count, plaza_data['total'], page))
                # print("insert city " + city['cityName'] + " len : " + str(len(plaza_list)) + " insertCount : " +
                #       str(insert_count) + "")
                if int(plaza_data['total']) < page * size:
                    break
                else:
                    page += 1
        except:
            print("except = " + str(city))
    db.close()


def get_city_list():
    city_response = urllib.request.urlopen('https://api.ffan.com/ffan/v3/cities')
    city_response_json_str = city_response.read().decode('utf-8')
    city_result = json.loads(city_response_json_str)
    return city_result['data']['cityList']


def get_current_time():
    return int(time.time() * 1000)
























