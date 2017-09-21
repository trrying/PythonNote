import pymysql
import requests

test_db = 1
official_db = 2
online_db = 3

# 启用配置
db_config = online_db

host = ""
port = ""
database_name = ""
user_name = ""
password = ""
charset = "utf8"


def get_info():
    return str("{'host':'" + host + "'," +
               "'port':'" + port + "'," +
               "'database_name':'" + database_name + "'," +
               "'user_name':'" + user_name + "'," +
               "'password':'" + password + "'," +
               "'charset':'" + charset + "'," +
               "}")

if db_config == test_db:
    # db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    print("user test_db")
    host = "192.168.1.4"
    user_name = "root"
    password = "12345"
    database_name = "spider"
    print(get_info())
elif db_config == official_db:
    # 地址10.10.41.149 账号spider 密码spider@svYVGKxC 数据库: spider_data
    print("user official_db")
    host = "10.10.41.149"
    user_name = "spider"
    password = "spider@svYVGKxC"
    database_name = "spider_data"
    print(get_info())
elif db_config == online_db:
    print("user online_db")
    host = "10.10.41.149"
    user_name = "front"
    password = "front@qazxsw3#edc"
    database_name = "mappush"
    print(get_info())


def get_db_config():

    # 打开数据库连接
    db = pymysql.connect(host, user_name, password, database_name, charset=charset)
    cursor = db.cursor()

    return db, cursor


if __name__ == '__main__':
    print(get_info())


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}


def request(url):
    response_str = requests.get(url, headers=headers).text.encode('latin-1').decode('unicode_escape').replace(
        "\n", "").replace("\t", "").replace("\r", "")
    return response_str


def request_content(url):
    return requests.get(url, headers=headers).content






