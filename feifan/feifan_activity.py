import urllib.request
import json
import pymysql
import sys
import util.time_utils
import threading
import math
import ffan_db_config


def get_data(thread_name, data_list):
    # 打开数据库连接
    db, cursor = ffan_db_config.get_db_config()

    print("plaza_list len : %d " % (len(data_list)))

    # base_coupons_list_url = "https://api.ffan.com/ffan/v1/city/coupons?size=%d&offset=%d&plazaId=%s&cityId=%s"
    base_coupons_list_url = "https://api.ffan.com/ffan/v1/city/activities?size=%s&offset=%s&plazaId=%s&cityId=%s"
    size = 50

    base_count_sql = "select count(*) from ffan_news where fp_p_id = '%(fp_p_id)s' and fn_aid = '%(fn_aid)s'"

    base_update_sql = """
                      update ffan_news set 
                      fn_title='%(fn_title)s', 
                      fn_description='%(fn_description)s', 
                      fn_subtitle='%(fn_subtitle)s', 
                      fn_logo='%(fn_logo)s', 
                      fn_start_time='%(fn_start_time)s', 
                      fn_end_time='%(fn_end_time)s', 
                      fn_update_time='%(fn_update_time)s' 
                      where fp_p_id = '%(fp_p_id)s' and fn_aid = '%(fn_aid)s'
                      """

    base_insert_sql = """
                      insert into ffan_news (
                      fn_title, 
                      fn_description, 
                      fn_subtitle, 
                      fn_logo,
                      fn_start_time, 
                      fn_end_time, 
                      fp_p_id, 
                      fn_aid, 
                      fn_create_time)
                      VALUES (
                      '%(fn_title)s', 
                      '%(fn_description)s', 
                      '%(fn_subtitle)s', 
                      '%(fn_logo)s', 
                      '%(fn_start_time)s', 
                      '%(fn_end_time)s', 
                      '%(fp_p_id)s',
                      '%(fn_aid)s',  
                      '%(fn_create_time)s')
                      """

    start_time = util.time_utils.get_current_time()

    for index, plaza in enumerate(data_list):
        offset = 0
        retry_count = 0
        while True:
            try:
                # 只重试2次
                if retry_count > 2:
                    break

                # 取出数据库查询的值
                plaza_id = plaza[0]
                plaza_name = plaza[1]
                plaza_city_id = plaza[2]
                plaza_city_name = plaza[3]

                # 拼接url，请求获取数据
                url = base_coupons_list_url % (size, offset, plaza_id, plaza_city_id)
                result_json_str = ffan_db_config.request(url)
                # print("result_json_str : " + result_json_str)

                # 解析json字符串
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

                    count_sql = base_count_sql % {'fp_p_id': data_bean['plazaId'], 'fn_aid': data_bean['id']}
                    cursor.execute(count_sql)
                    count_sql_result = cursor.fetchone()
                    try:
                        if count_sql_result[0] > 0:
                            # print("update data_bean : %s" % (str(data_bean)))
                            update_sql = base_update_sql % {
                                'fn_title': data_bean['title'],
                                'fn_description': data_bean['description'],
                                'fn_subtitle': data_bean['subtitle'],
                                'fn_logo': data_bean['pic'],
                                'fn_start_time': data_bean['startDate'],
                                'fn_end_time': data_bean['endDate'],
                                'fn_update_time': util.time_utils.get_current_time(),
                                'fp_p_id': data_bean['plazaId'],
                                'fn_aid': data_bean['id']
                            }
                            # print(update_sql)
                            update_count += cursor.execute(update_sql)
                        else:
                            # print("insert data_bean : %s" % (str(data_bean)))
                            insert_sql = base_insert_sql % {
                                'fn_title': data_bean['title'],
                                'fn_description': data_bean['description'],
                                'fn_subtitle': data_bean['subtitle'],
                                'fn_logo': data_bean['pic'],
                                'fn_start_time': data_bean['startDate'],
                                'fn_end_time': data_bean['endDate'],
                                'fp_p_id': data_bean['plazaId'],
                                'fn_aid': data_bean['id'],
                                'fn_create_time': util.time_utils.get_current_time()
                            }
                            # print(insert_sql)
                            insert_count += cursor.execute(insert_sql)
                        db.commit()
                    except Exception as e:
                        print(e)
                        db.rollback()
                        print("execute sql fail " + plaza_city_name + " " + plaza_name, sys.exc_info())
                print("ffan_news  operate db threadName : %s  data.len : %d  progress : %s  result_data len : %s  insertCount : %d  updateCount : %d  offset : %d  retry_count : %d"
                      % (thread_name, len(data_list), str(int((index+1) / (len(data_list))*100))+"%", len(result_data_list), insert_count, update_count, offset, retry_count))
                if int(result_data['info']['more']) > 0:
                    offset += size
                else:
                    break
            except Exception as e:
                print(e)
                print(sys.exc_info())
                retry_count += 1
    db.close()
    print("activity list operate db threadName : %s 耗时：%s 秒" % (thread_name, (util.time_utils.get_current_time() - start_time)))


# 开启线程类
class OperateThread(threading.Thread):
    def __init__(self, thread_id, data_list):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.dataList = data_list

    def run(self):
        get_data(self.threadId, self.dataList)


# thread_count 大于0开启线程，否则直接在线程运行
def start_get_data(thread_count=0):
    # 打开数据库连接
    db, cursor = ffan_db_config.get_db_config()

    select_sql = "select fp_p_id,fp_p_name,fp_city_id,fp_city from ffan_poi"
    cursor.execute(select_sql)
    sql_result = cursor.fetchall()
    print("activity plaza size : %s" % (len(sql_result)))

    if thread_count > 0:
        thread_data_size = math.ceil(len(sql_result) / thread_count)
        for i in range(thread_count):
            begin = i * thread_data_size
            end = (i + 1) * thread_data_size
            OperateThread(i+1, sql_result[begin:end]).start()
    else:
        get_data('caller thread', sql_result)


if __name__ == "__main__":
    start_get_data(5)











