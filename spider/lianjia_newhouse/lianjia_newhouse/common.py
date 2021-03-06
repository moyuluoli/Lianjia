# -*- coding: utf-8 -*-
import requests
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.101 Safari/537.36',
    'Cookie': 'lianjia_uuid=60768cd4-5897-47e9-83db-d0518431cc0f; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216a1a94a19d2f1-04621151e2329-1b2e1209-1049088-16a1a94a19e2b6%22%2C%22%24device_id%22%3A%2216a1a94a19d2f1-04621151e2329-1b2e1209-1049088-16a1a94a19e2b6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lianjia_ssid=86e287ff-c6a0-483d-96ee-7a51a4bc8c89; select_city=110000; search_position=search_result; lj_newh_session=eyJpdiI6ImJOVHZHeXorQXhWT2dFNG1lVmN5QkE9PSIsInZhbHVlIjoidFwvaXBoQW4yajFoSExXKzRpV1BETzFBSkpMXC9uREFGSU5CRXVrdTlVS2xHVWFLWUpOUXQzT0ptVnk0YllER0xNOElMR0laRDN1U1Q3Nm14dk9qNTFTQT09IiwibWFjIjoiOGQwNzRkODQ4NDljNGRiZjdkYzdjNjY1YjYzYjI5M2I4MzE5Yjk2MjU4NTlmMjNlYWY5ZjJlOGFhZTE2NTk3YSJ9'
}
# 房产数据标记
# 该字段不存在
NOT_EXIST_NUM = -1
NOT_EXIST_STR = ''
NOT_EXIST_LIST = []
DEFAULT_NEWHOUSE_PAGE = 20
# 部分以下城市无新房数据，删除这些城市的url
NO_NEWHOUSE = ['安庆', '马鞍山', '芜湖', '福州', '江门', '湛江', '北海', '桂林', '柳州', '南宁',
               '兰州', '黄石', '襄阳', '宜昌', '常德', '岳阳', '株洲', '唐山', '开封', '洛阳',
               '新乡', '许昌', '哈尔滨', '常州', '淮安', '昆山', '盐城', '吉林', '赣州', '九江',
               '吉安', '上饶', '丹东', '银川', '达州', '凉山', '绵阳', '南充', '临沂', '潍坊',
               '淄博', '宝鸡', '汉中', '咸阳', '金华', '宁波', '台州', '温州'
               ]


def all_city_map():
    response = requests.get('https://www.lianjia.com/city/', headers=header)
    data = re.findall(re.compile('<li><a href="https://(.+?).lianjia.com/">(.+?)</a></li>'),
                      response.text)
    city_map = {}
    for tuple in data:
        city_map[tuple[1]] = 'https://{}.lianjia.com/'.format(tuple[0])
    for city in NO_NEWHOUSE:
        city_map.pop(city)
    return city_map


def get_all_city():
    response = requests.get('https://www.lianjia.com/city/', headers=header)
    data = re.findall(re.compile('<li><a href="https://(.+?).lianjia.com/">(.+?)</a></li>'),
                      response.text)
    all_city_url_list = ['https://{}.lianjia.com/'.format(tuple[0]) for tuple in data]
    return all_city_url_list


def get_new_house_page(url):
    response = requests.get("{}/loupan/pg1/".format(url), headers=header).text
    page_num = re.findall(re.compile('<span class="value">(.+?)</span>'), response)
    if len(page_num) > 0:
        return int(int(page_num[0]) / 10 + 1)
    else:
        return DEFAULT_NEWHOUSE_PAGE
