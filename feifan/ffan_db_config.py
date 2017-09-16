
test_db_config = 1
official_db_config = 2

# 启用配置
db_config = official_db_config

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

if db_config == test_db_config:
    # db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
    print("user test_db_config")
    host = "192.168.1.4"
    user_name = "root"
    password = "12345"
    database_name = "spider"
    print(get_info())
elif db_config == official_db_config:
    # 地址10.10.41.149 账号spider 密码spider@svYVGKxC 数据库: spider_data
    print("user official_db_config")
    host = "10.10.41.149"
    user_name = "spider"
    password = "spider@svYVGKxC"
    database_name = "spider_data"
    print(get_info())

if __name__ == '__main__':
    print(get_info())












