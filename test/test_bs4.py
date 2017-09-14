# coding:utf - 8
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse

# html = urlopen("http://h5.ffan.com/app/coupon?cid=20170706101934&cityId=110100&plazaId=1000265&display_type=html")
html = urlopen("http://h5.ffan.com/app/activity?plazaId=1100796&cityId=110100&aid=93170&display_type=html")
bs = BeautifulSoup(html, "lxml")  # 将html对象转化为BeautifulSoup对象
print(bs.title)  # 输出这个网页中的标题

# 获取门店名称和地址
name_list = bs.find("div", {"class": "txt"})
# print(name_list)
print(name_list.find("h3").text)
print(name_list.find("p").text)


print()

# 获取详情
more_detail_list = bs.find("div", {"class": "pd10 layout-detail-content"}).findAll("p")
more_detail = ""
for detail in more_detail_list:
    more_detail += detail.text.replace("\r", "").replace("\n", "").replace("\t", "") + "\n"
print(more_detail)

# 获取logo
logo = bs.find("img", {"class": "lazyImgDefault"})['data-original']
print(logo)

# 获取电话
phoneUrl = bs.find("i", {"class": "iconfont gray icon-telephone"}).parent["href"]
phone_param = parse.parse_qs(parse.urlparse(phoneUrl).query)['phone'][0]
print(phone_param)

# 获取经纬度 href="wandaappfeifan://app/outside_map?name=总服务台（石景山万达广场）&longitude=116.225836&latitude=39.906344"
locationUrl = bs.find("i", {"class": "iconfont gray icon-fly"}).parent["href"]
print(locationUrl)
location_params = parse.parse_qs(parse.urlparse(locationUrl).query)
print(location_params)
lng = location_params['longitude'][0]
lat = location_params['latitude'][0]
print(lng+","+lat)





















