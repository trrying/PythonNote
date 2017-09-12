import time


def get_time(time_str):
    return int(time.mktime(time.strptime(time_str, "%Y.%m.%d"))*1000)


def get_current_time():
    return int(time.time() * 1000)
