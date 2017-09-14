
# https://h5.ffan.com/app/activity?plazaId=1100796&cityId=110100&aid=93170
# http://m.ffan.com/#/detail/coupon/20170706101934?cityId=110100&plazaId=1000265&_k=5712jh

import urllib
from urllib import request

page = 1
url = "http://h5.ffan.com/app/activity?plazaId=1100796&cityId=110100&aid=93170&display_type=html"
# url = "http://h5.ffan.com/app/coupon?cid=20170825150737&cityId=110100&plazaId=1000265&display_type=html"


# url = 'http://www.baidu.com'
def getHTML(url):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Host': 'h5.ffan.com',
'charset': 'UTF-8',
'Origin': 'http://m.ffan.com',
'Proxy-Connection': 'keep-alive',
'Referer': 'http://m.ffan.com/',
'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36}'}

    req = request.Request(url)
    return request.urlopen(req)


try:
    response = getHTML(url)
    print(response.read().decode('utf-8'))
except urllib.request.URLError as e:
        print(e)












