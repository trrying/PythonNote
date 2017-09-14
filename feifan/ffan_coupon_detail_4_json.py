from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import pymysql
import threading
import math


def get_detail(thread_name, data_list):
    # 打开数据库连接
    db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf-8')
    cursor = db.cursor()
    print("data_list len : %d" % (len(data_list)))

    base_url = "http://h5.ffan.com/app/coupon?cid=%s&cityId=%s&plazaId=%s&display_type=json"

    base_update_sql = """update ffan_coupon set fc_apply_store='%s', fc_more_details='%s', fc_operate_time='%s' WHERE fp_p_id = '%s' and fc_aid = '%s'"""

    for index, data_bean in enumerate(data_list):
        retry_count = 0
        while True:
            try:
                if retry_count > 2:
                    break
                cid = data_bean[0]
                city_id = data_bean[1]
                plaza_id = data_bean[2]

                url = base_url % (cid, city_id, plaza_id)
                html = urlopen(url)
                print(html)
                break
            except BaseException as e:
                print(e)

























































