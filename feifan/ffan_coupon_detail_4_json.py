from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from urllib import parse
import pymysql
import threading
import math
import util.time_utils
import ffan_db_config
import json
from pyquery import PyQuery
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def get_detail(thread_name, data_list):
    # 打开数据库连接
    db = pymysql.connect(ffan_db_config.host, ffan_db_config.user_name, ffan_db_config.password,
                         ffan_db_config.database_name, charset=ffan_db_config.charset)
    cursor = db.cursor()
    print("data_list len : %d" % (len(data_list)))

    base_url = "http://h5.ffan.com/app/coupon?cid=%(cid)s&cityId=%(cityId)s&plazaId=%(plazaId)s&display_type=json"

    base_update_sql = """update ffan_coupon set 
                                        fc_apply_store='%(fc_apply_store)s', 
                                        fc_more_details='%(fc_more_details)s', 
                                        fc_operate_time='%(fc_operate_time)s' 
                                        WHERE fp_p_id = '%(fp_p_id)s' and fc_aid = '%(fc_aid)s'
                                        """

    for index, data_bean in enumerate(data_list):
        retry_count = 0
        while True:
            try:
                if retry_count > 2:
                    break
                cid = data_bean[0]
                city_id = data_bean[1]
                plaza_id = data_bean[2]

                # url = base_url % (cid, city_id, plaza_id)
                url = base_url % {'cid': cid, 'cityId': city_id, 'plazaId': plaza_id}
                print(url)
                response_str = requests.get(url, headers=headers).text.encode('latin-1').decode('unicode_escape')
                print("response_str : " + response_str)
                print()

                # response_str = PyQuery(response_str).text()
                # print("PyQuery : "+response_str)

                response_bean = json.loads(response_str)
                print("response_bean + "+str(response_bean))

                fc_apply_store = {}
                fc_more_details = ""
                fc_limit = ""

                # 获取门店名称
                try:
                    fc_name = response_bean['coupon_detail']['store_detail']['storeName']
                    fc_apply_store['name'] = fc_name
                except Exception as e:
                    print(e)

                # 获取门店地址
                try:
                    fc_address = response_bean['coupon_detail']['store_detail']['storeAddress']
                    fc_apply_store['address'] = fc_address
                except Exception as e:
                    print(e)

                # 获取logo
                try:
                    logo = "https://" + response_bean['coupon_detail']['store_detail']['storePicsrcUrl']
                    fc_apply_store['logo'] = logo
                except Exception as e:
                    print(e)

                # 获取电话 storePhone
                try:
                    phone = response_bean['coupon_detail']['store_detail']['storePicsrcUrl']
                    fc_apply_store['phone'] = phone
                except Exception as e:
                    print(e)

                # 获取经纬度
                try:
                    locationUrl = bs.find("i", {"class": "iconfont gray icon-fly"}).parent["href"]
                    location_params = parse.parse_qs(parse.urlparse(locationUrl).query)
                    lng = location_params['longitude'][0]
                    lat = location_params['latitude'][0]
                    fc_apply_store['location'] = lng + "," + lat
                except Exception as e:
                    print(e)

                # 获取详情
                try:
                    more_detail_list = bs.find("div", {"class": "couponDsp pdlr10"}).findAll("p")
                    more_detail = ""
                    for detail in more_detail_list:
                        more_detail += detail.text.replace("\r", "").replace("\n", "").replace("\t", "") + "\n"
                    fc_more_details = more_detail
                except Exception as e:
                    print(e)

                # 获取优惠卷领取数量限制说明
                try:
                    fc_limit = bs.find("span", {"class": "limit"}).text
                except Exception as e:
                    print(e)

                break
            except BaseException as e:
                print(e)
                retry_count += 1


class OperateThread(threading.Thread):
    def __init__(self, thread_id, data_list):
        threading.Thread.__init__(self)
        self.threadId = thread_id
        self.dataList = data_list

    def run(self):
        get_detail(self.threadId, self.dataList)


def get_all_coupon():
    thread_count = 5
    # 打开数据库连接
    db = pymysql.connect(ffan_db_config.host, ffan_db_config.user_name, ffan_db_config.password,
                         ffan_db_config.database_name, charset=ffan_db_config.charset)
    cursor = db.cursor()
    select_sql = "SELECT c.fc_aid,p.fp_city_id,c.fp_p_id FROM ffan_poi AS p, ffan_coupon c WHERE p.fp_p_id = c.fp_p_id"
    cursor.execute(select_sql)
    sql_result = cursor.fetchall()
    print("coupon size : %s" % (len(sql_result)))

    thread_data_size = math.ceil(len(sql_result) / thread_count)
    OperateThread(1, sql_result).start()
    # for i in range(thread_count):
    #     begin = i * thread_data_size
    #     end = (i + 1) * thread_data_size
    #     OperateThread(i+1, sql_result[begin:end]).start()

if __name__ == "__main__":
    get_all_coupon()























































