from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import pymysql
import threading
import math
import util.time_utils

def get_detail(thread_name, data_list):
    # 打开数据库连接
    db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    cursor = db.cursor()
    print("data_list len : %d " % (len(data_list)))

    baseUrl = "http://h5.ffan.com/app/activity?aid=%s&cityId=%s&plazaId=%s&display_type=html"

    base_update_sql = """update ffan_news set fn_apply_sotre='%s', fn_details='%s' fn_update_time='%s' WHERE fp_p_id = '%s' and fn_aid = '%s'"""

    for index, data_bean in enumerate(data_list):
        retry_count = 0
        while True:
            try:
                if retry_count > 2:
                    break
                aid = data_bean[0]
                city_id = data_bean[1]
                plaza_id = data_bean[2]

                url = baseUrl % (aid, city_id, plaza_id)
                # print("url "+url)
                html = urlopen(url)
                # print("html "+str(html))
                bs = BeautifulSoup(html, "lxml")

                # {name:''门店名称'',address:''门店地址'', logo:''门店logo地址'',phone:''门店电话'', location:''经度,纬度''}
                fc_apply_store = {}
                fc_more_details = ""

                # 获取门店名称和地址
                try:
                    name_list = bs.find("div", {"class": "txt"})
                    fc_name = name_list.find("h3").text
                    fc_address = name_list.find("p").text

                    fc_apply_store['name'] = fc_name
                    fc_apply_store['address'] = fc_address
                except Exception as e:
                    print(e)

                # 获取logo
                try:
                    logo = "https://" + bs.find("img", {"class": "lazyImgDefault"})['data-original']
                    fc_apply_store['logo'] = logo
                except Exception as e:
                    print(e)

                # 获取电话
                try:
                    phone_url = bs.find("i", {"class": "iconfont gray icon-telephone"}).parent["href"]
                    phone = parse.parse_qs(parse.urlparse(phone_url).query)['phone'][0]
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
                    more_detail_list = bs.find("div", {"class": "pd10 layout-detail-content"}).findAll("p")
                    more_detail = ""
                    for detail in more_detail_list:
                        more_detail += detail.text.replace("\r", "").replace("\n", "").replace("\t", "") + "\n"
                    fc_more_details = more_detail
                except Exception as e:
                    print(e)

                update_count = 0
                if len(fc_apply_store) | len(fc_more_details):
                    update_sql = ""
                    try:
                        fc_apply_store_json = ""
                        if len(fc_apply_store):
                            fc_apply_store_json = str(fc_apply_store).replace("'", "\"")
                        update_sql = base_update_sql % (fc_apply_store_json, fc_apply_store_json, util.time_utils.get_current_time(), plaza_id, aid)
                        # print("update_sql : " + update_sql)
                        update_count = cursor.execute(update_sql)
                        db.commit()
                    except Exception as e:
                        print(e)
                        db.rollback()
                        print("execute sql fail " + update_sql)
                print("ffan_news  update db threadName : %s  data.len : %d  progress : %s  updateCount : %d  retry_count : %d"
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
    select_sql = "SELECT n.fn_aid,p.fp_city_id,n.fp_p_id FROM ffan_poi AS p, ffan_news n WHERE p.fp_p_id = n.fp_p_id"
    cursor.execute(select_sql)
    sql_result = cursor.fetchall()
    print("coupon size : %s" % (len(sql_result)))

    thread_data_size = math.ceil(len(sql_result) / thread_count)
    # OperateThread(1, sql_result).start()
    for i in range(thread_count):
        begin = i * thread_data_size
        end = (i + 1) * thread_data_size
        OperateThread(i+1, sql_result[begin:end]).start()


get_all_coupon()






























