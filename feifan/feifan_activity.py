import urllib.request
import json
import pymysql
import sys
import util.time_utils
import threading
import math


def get_data(thread_name, data_list):
    # 打开数据库连接
    db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    cursor = db.cursor()

    print("plaza_list len : %d " % (len(data_list)))

    # base_coupons_list_url = "https://api.ffan.com/ffan/v1/city/coupons?size=%d&offset=%d&plazaId=%s&cityId=%s"
    base_coupons_list_url = "https://api.ffan.com/ffan/v1/city/activities?size=%s&offset=%s&plazaId=%s&cityId=%s"
    size = 50

    base_count_sql = "select count(*) from ffan_news where fp_p_id = '%s' and fn_aid = '%s'"

    base_update_sql = """update ffan_news set fn_title='%s', fn_description='%s', fn_subtitle='%s', fn_logo='%s'
                      , fn_start_time='%s', fn_end_time='%s', fn_update_time='%s' where fp_p_id = '%s' and fn_aid = '%s'
                      """

    base_insert_sql = """insert into ffan_news (fn_title, fn_description, fn_subtitle, fn_logo,
                      fn_start_time, fn_end_time, fn_aid, fp_p_id, fn_create_time)
                      VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""

    for index, plaza in enumerate(data_list):
        offset = 0
        retry_count = 0
        while True:
            try:
                # 只重试2次
                if retry_count > 2:
                    break
                plaza_id = plaza[0]
                plaza_name = plaza[1]
                plaza_city_id = plaza[2]
                plaza_city_name = plaza[3]

                url = base_coupons_list_url % (size, offset, plaza_id, plaza_city_id)
                result_response = urllib.request.urlopen(url)
                result_json_str = result_response.read().decode('utf-8')
                response_result = json.loads(result_json_str)
                result_data = response_result['data']
                result_data_list = result_data['list']
                insert_count = 0
                update_count = 0
                for data_bean in result_data_list:
                    # print("data_bean : %s" % (str(data_bean)))
                    data_bean['plazaId'] = plaza_id
                    data_bean['startDate'] = util.time_utils.get_time(data_bean['startDate'])
                    data_bean['endDate'] = util.time_utils.get_time(data_bean['endDate'])
                    data_bean['title'] = data_bean['title'].replace("'", "''")
                    data_bean['description'] = data_bean['description'].replace("'", "''")
                    data_bean['subtitle'] = data_bean['subtitle'].replace("'", "''")

                    count_sql = base_count_sql % (data_bean['plazaId'], data_bean['id'])
                    cursor.execute(count_sql)
                    count_sql_result = cursor.fetchone()
                    try:
                        if count_sql_result[0] > 0:
                            # print("update data_bean : %s" % (str(data_bean)))
                            update_sql = base_update_sql % (data_bean['title'], data_bean['description'], data_bean['subtitle'], data_bean['pic'],
                                                            data_bean['startDate'], data_bean['endDate'], util.time_utils.get_current_time(), data_bean['plazaId'], data_bean['id'])
                            # print(update_sql)
                            update_count += cursor.execute(update_sql)
                        else:
                            # print("insert data_bean : %s" % (str(data_bean)))
                            insert_sql = base_insert_sql % (data_bean['title'], data_bean['description'], data_bean['subtitle'], data_bean['pic'],
                                                            data_bean['startDate'], data_bean['endDate'], data_bean['id'], data_bean['plazaId'], util.time_utils.get_current_time())
                            # print(insert_sql)
                            insert_count += cursor.execute(insert_sql)
                        db.commit()
                    except:
                        db.rollback()
                        print("execute sql fail " + plaza_city_name + " " + plaza_name, sys.exc_info())
                print("ffan_news  operate db threadName : %s  data.len : %d  progress : %s  result_data len : %s  insertCount : %d  updateCount : %d  offset : %d  retry_count : %d"
                      % (thread_name, len(data_list), str(int((index+1) / (len(data_list))*100))+"%", len(result_data_list), insert_count, update_count, offset, retry_count))
                if int(result_data['info']['more']) > 0:
                    offset += size
                else:
                    break
            except:
                print(sys.exc_info())
                retry_count += 1
    db.close()


class OperateThread(threading.Thread):
    def __init__(self, thread_id, data_list):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.dataList = data_list

    def run(self):
        get_data(self.threadId, self.dataList)


def start_get_data():
    thread_count = 5
    # 打开数据库连接
    db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    cursor = db.cursor()
    select_sql = "select fp_p_id,fp_p_name,fp_city_id,fp_city from ffan_poi"
    cursor.execute(select_sql)
    sql_result = cursor.fetchall()
    print("plaza size : %s" % (len(sql_result)))

    thread_data_size = math.ceil(len(sql_result) / thread_count)

    for i in range(thread_count):
        begin = i * thread_data_size
        end = (i + 1) * thread_data_size
        OperateThread(i+1, sql_result[begin:end]).start()


start_get_data()











