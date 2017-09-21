import threading
import feifan_poi
import feifan_coupon
import feifan_detail_coupon
import feifan_activity
import feifan_detail_activity
import time
import datetime


# 获取广场列表
def get_poi():
    feifan_poi.get_plaza()


def get_coupon():
    # 获取列表优惠卷
    feifan_coupon.start_get_coupon()
    # 获取优惠卷详情
    feifan_detail_coupon.get_all_coupon()
    # 获取图片上传七牛
    pass


def get_activity():
    # 获取列表活动
    feifan_activity.start_get_data()
    # 获取活动详情
    feifan_detail_activity.get_all_coupon()
    # 获取图片上传七牛
    pass


def get_all():
    poi_time = time.time()
    get_poi()
    poi_time = time.time() - poi_time

    coupon_time = time.time()
    get_coupon()
    coupon_time = time.time() - coupon_time

    activity_time = time.time()
    get_activity()
    activity_time = time.time() - activity_time

    print("耗时  poi_time : %s  coupon_time : %s  activity_time : %s ", (poi_time, coupon_time, activity_time))


# 开启优惠卷数据抓取线程类
class GetCouponThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # 获取列表优惠卷
        feifan_coupon.start_get_coupon()
        # 获取优惠卷详情
        feifan_detail_coupon.get_all_coupon()
        # 获取图片上传七牛
        pass


# 开启活动数据抓取线程类
class GetActivityThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # 获取列表活动
        feifan_activity.start_get_data()
        # 获取活动详情
        feifan_detail_activity.get_all_coupon()
        # 获取图片上传七牛


# 开启活动数据抓取线程类
class GetPoiThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        # 获取广场列表
        feifan_poi.get_plaza()


if __name__ == '__main__':
    last_run_day = 0
    while 1:
        weekday = time.strftime("%w", time.localtime())
        print("main time : %s  weekday : %s" % (str(datetime.datetime.now()), weekday))
        # if weekday == 1:
        #     GetPoiThread().start()
        # if weekday in (1, 3, 5):
        #     GetCouponThread().start()
        #     GetActivityThread().start()
        # 周 1/3/5 去获取更新数据库
        if weekday in (1, 3, 5) and weekday != last_run_day:
            last_run_day = weekday
            print("run")
            get_all()
        # 2个小时调用一次
        time.sleep(60 * 60 * 2)
























