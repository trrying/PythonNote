import urllib.request
import json
import pymysql
import time
import ffan_db_config
import requests


def get_plaza():
    city_list = get_city_list()

    print("cityList.len : " + str(len(city_list)))

    base_url = "https://api.ffan.com/ffan/v1/city/locationSeek?cityId=%s&size=%s&page=%s"
    size = 50

    # 打开数据库连接
    db, cursor = ffan_db_config.get_db_config()
    headers = ffan_db_config.headers

    # 插入语句
    baseInsertSql = """
    insert into ffan_poi (fp_p_id, fp_p_name, fp_p_address, fp_city, fp_city_id, fp_create_time)
    VALUES ('%(fp_p_id)s', '%(fp_p_name)s', '%(fp_p_address)s', '%(fp_city)s', '%(fp_city_id)s', '%(fp_create_time)s')
    """

    base_count_sql = "select count(*) from ffan_poi where fp_p_id = '%(fp_p_id)s'"

    base_update_sql = """
                          update ffan_poi set 
                          fp_p_name='%(fp_p_name)s', 
                          fp_p_address='%(fp_p_address)s', 
                          fp_city='%(fp_city)s', 
                          fp_city_id='%(fp_city_id)s', 
                          fp_update_time='%(fp_update_time)s' 
                          WHERE fp_p_id = '%(fp_p_id)s'
                          """
    # 遍历所有城市，查询城市的所有广场
    for city in city_list:
        try:
            page = 1
            city_id = city['cityId']
            # 接口最多返回50条，要循环获取所有广场；如果当前记录获取条数大于等于50，继续尝试获取下一次
            while True:

                # 拼接url，请求获取json字符串数据
                url = base_url % (city_id, str(size), str(page))
                plaza_result_json_str = requests.get(url, headers=headers).text.encode('latin-1').decode('unicode_escape').replace("\n", "").replace("\t", "").replace("\r", "")

                # 解析json数据，获取最终的广场列表
                plaza_result = json.loads(plaza_result_json_str)
                plaza_data = plaza_result['data']
                plaza_list = plaza_data['list']

                # 统计插入、更新条数，方便记录日志
                insert_count = 0
                update_count = 0

                # 询函广场列表，插入或者更新数据
                for plaza in plaza_list:
                    try:
                        # 查询当前广场是否有数据，有就更新，没有就插入
                        select_sql = base_count_sql % {'fp_p_id': plaza['id']}
                        cursor.execute(select_sql)
                        count_plaza = cursor.fetchone()

                        if count_plaza[0]:
                            update_sql = base_update_sql % {'fp_p_name': plaza['plazaName'],
                                                            'fp_p_address': plaza['plazaAddress'],
                                                            'fp_city': plaza['cityName'],
                                                            'fp_city_id': plaza['cityId'],
                                                            'fp_update_time': get_current_time(),
                                                            'fp_p_id': plaza['id']}
                            update_count += cursor.execute(update_sql)
                        else:
                            insert_sql = baseInsertSql % {'fp_p_id': plaza['id'],
                                                          'fp_p_name': plaza['plazaName'],
                                                          'fp_p_address': plaza['plazaAddress'],
                                                          'fp_city': plaza['cityName'],
                                                          'fp_city_id': plaza['cityId'],
                                                          'fp_create_time': get_current_time()}
                            insert_count += cursor.execute(insert_sql)
                        db.commit()
                    except BaseException as e:
                        db.rollback()
                        print("execute sql fail " + plaza['cityName'] + " " + plaza['plazaName'] + str(e))

                # 输入记录
                print("insert city : %s  len : %d  insertCount : %d  updateCount : %d  total : %s  page : %d"
                      % (city['cityName'], len(plaza_list), insert_count, update_count, plaza_data['total'], page))

                # 如果获取广场数小于一页数据量，直接跳出循环，查询下一个广场列表
                if int(plaza_data['total']) < page * size:
                    break
                else:
                    page += 1

        except BaseException as e:
            print("except = " + str(city) + " error : " + str(e))
    db.close()


# 获取所有城市列表
def get_city_list():
    city_response = urllib.request.urlopen('https://api.ffan.com/ffan/v3/cities')
    city_response_json_str = city_response.read().decode('utf-8')
    city_result = json.loads(city_response_json_str)
    return city_result['data']['cityList']


# 获取当前时间戳，精确到毫秒
def get_current_time():
    return int(time.time() * 1000)


if __name__ == "__main__":
    get_plaza()






















