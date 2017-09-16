

test_db_config = 1
official_db_config = 2

# 启用配置
db_config = test_db_config

host = ""
port = ""
database_name = ""
user_name = ""
password = ""
charset = "utf8"

def get_db_config():
    db_config_set = DBConfig()
    if db_config == test_db_config:
        # db = pymysql.connect("192.168.1.4", "root", "12345", "spider", charset='utf8')
        print("user test_db_config")
        db_config_set.host = "192.168.1.4"
        db_config_set.user_name = "root"
        db_config_set.password = "12345"
        db_config_set.database_name = "spider"
    elif db_config == official_db_config:
        # 地址10.10.41.149 账号spider 密码spider@svYVGKxC 数据库: spider_data
        print("user official_db_config")
        db_config_set.host = "10.10.41.149"
        db_config_set.user_name = "spider"
        db_config_set.password = "spider@svYVGKxC"
        db_config_set.database_name = "spider_data"
    return db_config_set


class DBConfig:
    host = ""
    port = ""
    database_name = ""
    user_name = ""
    password = ""
    charset = "utf8"

    def get_info(self):
        return str("{'host':'" + self.host + "'," +
                   "'port':'" + self.port + "'," +
                   "'database_name':'" + self.database_name + "'," +
                   "'user_name':'" + self.user_name + "'," +
                   "'password':'" + self.password + "'," +
                   "'charset':'" + self.charset + "'," +
                   "}")


if __name__ == '__main__':
    print(get_db_config().get_info())













