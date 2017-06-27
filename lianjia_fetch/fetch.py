#!/bin/bash/python
#! -*- encoding:utf8 -*-

from bs4 import BeautifulSoup as Bs
import requests as Req
import re

URL = "http://sh.lianjia.com/ershoufang/d100"

def fetch_prop_list(url=URL):
    """Fetch the house property list from LianJia Shanghai"""
    if url is None:
        url = URL
    http_resp = Req.get(url);
    soup = Bs(http_resp.text, "lxml")
    prop_list = soup.find(class_="js_fang_list")
    return prop_list


def parse_prop_list(prop_list):
    """parse BeautifulSoap list into prop info list """
    # TODO param check
    ret_list = [];
    raw_list = prop_list.find_all("li")
    for item in raw_list:
        prop = parse_prop_info(item)
        ret_list.append(prop)
    return ret_list

def parse_prop_info(prop):
    """parse BeautifulSoap list into prop info list """
    item = {}
    city = "上海"
    name = prop.find(class_="text link-hover-green js_triggerGray js_fanglist_title")
    price = prop.find(class_="total-price strong-num")
    price_unit = prop.find(class_="unit")
    size_info = prop.find(class_="info-col row1-text")
    district_info = prop.find(class_="info-col row2-text")

    item['price'] = price.text
    item['name'] = name.text
    item['price_unit'] = price_unit.text
    parse_prop_size_info(size_info.text, item)
    parse_prop_distric_and_year(district_info.text, item)

    return item

def parse_prop_distric_and_year(str, item={}):
    """解析房子 小区和年限，比如： 东陆新村六街坊 | 浦东 | 金桥 | 1995年建
    """
    sep_p_str = r'\s*\|\s*'.decode('utf8')
    raw_list = re.split(sep_p_str, str)
    list = []
    for r_item in raw_list:
        list.append(r_item.strip())
    item.update({'addr' : list[0].encode("utf8")})
    item.update({'district' : list[1].encode("utf8")})
    item.update({'town' : list[2].encode("utf8")})
    if len(list) >= 4:
        year_p_str = r'\d+(?=年)'
        m = re.search(year_p_str, list[3].encode("utf8"))
        if m:
            item.update({'year' : int(m.group())})
    else:
        item.update({'year' : None})
    return item

def parse_prop_size_info(str, item):
    """解析房间大小和方位，比如： 1室1厅 | 57.5平 | 高区/6层 | 朝南
    """
    living_room_pattern_str = r'\d+(?=室)'.decode('utf8')
    room_pattern_str = r'(?<=室)\d+(?=厅)'.decode('utf8')
    size_pattern_str = r'(\d+|\d+\.\d+)(?=平)'.decode('utf8')
    total_floor_pattern_str =  r'(?<=\/)(\d+)(?=层)'.decode('utf8')
    floor_position_pattern_str =  r'\W(?=区)'.decode('utf8')
    build_face_pattern_str = r'(?<=朝)(\W)'.decode('utf8')

    living_room =  parse_helper(str, living_room_pattern_str)
    item['living_room_num'] = int(living_room)
    room_pattern =  parse_helper(str, room_pattern_str)
    item['room_num'] = int(room_pattern)
    size =  parse_helper(str, size_pattern_str)
    item['size'] = float(size)
    total_floor =  parse_helper(str, total_floor_pattern_str)
    item['total_floor'] = int(total_floor) if total_floor is not None else None
    floor_position =  parse_helper(str, floor_position_pattern_str)
    item['floor_position'] = floor_position
    build_face =  parse_helper(str, build_face_pattern_str)
    item['build_face'] = build_face


def parse_helper(str, pattern_str):
    p = re.compile(pattern_str)
    m = p.search(str)
    if m:
        return m.group()
    else:
        return None

if __name__ == "__main__":
    prop_list = fetch_prop_list()
    list = parse_prop_list(prop_list)
    for item in list:
        print item
