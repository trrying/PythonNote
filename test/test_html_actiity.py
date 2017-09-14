from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import re

url = "http://h5.ffan.com/app/activity?aid=147891&cityId=530100&plazaId=1102746&display_type=html"

html = urlopen(url)
bs = BeautifulSoup(html, 'lxml')

more_detail_list = ""

# 获取详情
try:
    more_detail_list = bs.find("div", {"class": "pd10 layout-detail-content"}).findAll("p")
    more_detail = ""
    for detail in more_detail_list:
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', detail.text)
        print(detail.text)
        print(dd)
        more_detail += detail.text.replace("\r", "").replace("\n", "").replace("\t", "") + "\n"
    fc_more_details = more_detail
except Exception as e:
    print(e)

print("fc_more_details='%s'" % (fc_more_details))












