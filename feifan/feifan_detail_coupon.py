from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import pymysql
import threading
import math
import util.time_utils
import ffan_db_config


def get_detail(thread_name, data_list):
    # 打开数据库连接
    db = pymysql.connect(ffan_db_config.host, ffan_db_config.user_name, ffan_db_config.password,
                         ffan_db_config.database_name, charset=ffan_db_config.charset)
    cursor = db.cursor()
    print("data_list len : %d " % (len(data_list)))

    baseUrl = "http://h5.ffan.com/app/coupon?cid=%s&cityId=%s&plazaId=%s&display_type=html"

    base_update_sql = """update ffan_coupon set fc_apply_store='%s', fc_more_details='%s', fc_limit='%s', fc_update_time='%s' WHERE fp_p_id = '%s' and fc_aid = '%s'"""

    for index, data_bean in enumerate(data_list):
        retry_count = 0
        while True:
            try:
                if retry_count > 2:
                    break
                cid = data_bean[0]
                city_id = data_bean[1]
                plaza_id = data_bean[2]

                url = baseUrl % (cid, city_id, plaza_id)
                # print("url "+url)
                html = urlopen(url)
                # print("html "+str(html))
                bs = BeautifulSoup(html, "lxml")

                # {name:''门店名称'',address:''门店地址'', logo:''门店logo地址'',phone:''门店电话'', location:''经度,纬度''}
                fc_apply_store = {}
                fc_more_details = ""
                fc_limit = ""

                # 获取门店名称和地址
                try:
                    name_list = bs.find("a", {"id": "storeName"})
                    fc_name = name_list.find("h3").text
                    fc_address = name_list.find("p").text

                    fc_apply_store['name'] = fc_name
                    fc_apply_store['address'] = fc_address
                except Exception as e:
                    print(e)

                # 获取logo
                try:
                    logo = "https://" + bs.find("a", {"id": "storeImg"}).find("img")['data-original']
                    fc_apply_store['logo'] = logo
                except Exception as e:
                    print(e)

                # 获取电话
                try:
                    phoneUrl = bs.find("i", {"class": "iconfont gray icon-telephone"}).parent["href"]
                    phone = parse.parse_qs(parse.urlparse(phoneUrl).query)['phone'][0]
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

                update_count = 0
                if len(fc_apply_store) | len(fc_more_details) | len(fc_limit):
                    update_sql = ""
                    try:
                        fc_apply_store_json = ""
                        if len(fc_apply_store):
                            fc_apply_store_json = str(fc_apply_store).replace("'", "\"")
                        update_sql = base_update_sql % (fc_apply_store_json, fc_more_details, fc_limit, util.time_utils.get_current_time(), plaza_id, cid)
                        # print("update_sql : " + update_sql)
                        update_count = cursor.execute(update_sql)
                        db.commit()
                    except Exception as e:
                        print(e)
                        db.rollback()
                        print("execute sql fail " + update_sql)
                print("ffan_coupon  update db threadName : %s  data.len : %d  progress : %s  updateCount : %d  retry_count : %d"
                    % (thread_name, len(data_list), str(int((index + 1) / (len(data_list)) * 100)) + "%",
                       update_count, retry_count))
                break
            except Exception as e:
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
    db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    cursor = db.cursor()
    select_sql = "SELECT c.fc_aid,p.fp_city_id,c.fp_p_id FROM ffan_poi AS p, ffan_coupon c WHERE p.fp_p_id = c.fp_p_id"
    cursor.execute(select_sql)
    sql_result = cursor.fetchall()
    print("coupon size : %s" % (len(sql_result)))

    thread_data_size = math.ceil(len(sql_result) / thread_count)
    # OperateThread(1, sql_result).start()
    for i in range(thread_count):
        begin = i * thread_data_size
        end = (i + 1) * thread_data_size
        OperateThread(i+1, sql_result[begin:end]).start()

if __name__ == "__main__":
    get_all_coupon()






























