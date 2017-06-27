#! -*- encoding:utf-8 -*-

import re
from base_crawler import BaseCrawler
from bs4 import BeautifulSoup as Bs


class LianJiaSHCrawler(BaseCrawler):
    """
        链家网上海爬虫
    """

    def __init__(self, url=None, headers=None, proxies=None):
        if url is None:
            url = "http://sh.lianjia.com/ershoufang/"
        super(LianJiaSHCrawler, self).__init__(url, headers, proxies)
        self.prop_list = []

    def crawl(self):
        raw_prop_list = self.fetch_prop_list()
        self.prop_list = self.parse_prop_list(raw_prop_list)
        return self.prop_list

    def fetch_prop_list(self):
        """
        Fetch the house property list from LianJia Shanghai
        """
        http_resp = self.fetch_content()
        soup = Bs(http_resp, "lxml")
        prop_list = soup.find(class_="js_fang_list")
        return prop_list

    def parse_prop_list(self, prop_list):
        """parse BeautifulSoap list into prop info list """
        # TODO param check
        ret_list = [];
        raw_list = prop_list.find_all("li")
        for item in raw_list:
            prop = self.parse_prop_info(item)
            ret_list.append(prop)
        return ret_list

    def parse_prop_info(self, prop):
        """parse BeautifulSoap list into prop info list """
        item = {}
        name = prop.find(class_="text link-hover-green js_triggerGray js_fanglist_title")
        price = prop.find(class_="total-price strong-num")
        price_unit = prop.find(class_="unit")
        size_info = prop.find(class_="info-col row1-text")
        district_info = prop.find(class_="info-col row2-text")

        item['price'] = price.text
        item['name'] = name.text
        item['price_unit'] = price_unit.text
        self.parse_prop_size_info(size_info.text, item)
        self.parse_prop_distric_and_year(district_info.text, item)

        return item

    def parse_prop_distric_and_year(self, strv, item={}):
        """解析房子 小区和年限，比如： 东陆新村六街坊 | 浦东 | 金桥 | 1995年建
        """
        sep_p_str = r'\s*\|\s*'.decode('utf8')
        raw_list = re.split(sep_p_str, strv)
        rlist = []
        for r_item in raw_list:
            rlist.append(r_item.strip())
        item.update({'addr': rlist[0]})
        item.update({'district': rlist[1]})
        item.update({'town': rlist[2]})
        if len(rlist) >= 4:
            year_p_str = r'\d+(?=年)'
            m = re.search(year_p_str, rlist[3].encode("utf8"))
            if m:
                item.update({'year': int(m.group())})
        else:
            item.update({'year': None})
        return item

    def old_parse_prop_distric_and_year(self, strv, item={}):
        """解析房子 小区和年限，比如： 东陆新村六街坊 | 浦东 | 金桥 | 1995年建
        """
        sep_p_str = r'\s*\|\s*'.decode('utf8')
        raw_list = re.split(sep_p_str, strv)
        rlist = []
        for r_item in raw_list:
            rlist.append(r_item.strip())
        item.update({'addr': rlist[0].encode("utf8")})
        item.update({'district': rlist[1].encode("utf8")})
        item.update({'town': rlist[2].encode("utf8")})
        if len(rlist) >= 4:
            year_p_str = r'\d+(?=年)'
            m = re.search(year_p_str, rlist[3].encode("utf8"))
            if m:
                item.update({'year': int(m.group())})
        else:
            item.update({'year': None})
        return item

    def parse_prop_size_info(self, str, item):
        """解析房间大小和方位，比如： 1室1厅 | 57.5平 | 高区/6层 | 朝南
        """
        living_room_pattern_str = r'\d+(?=室)'.decode('utf8')
        room_pattern_str = r'(?<=室)\d+(?=厅)'.decode('utf8')
        size_pattern_str = r'(\d+|\d+\.\d+)(?=平)'.decode('utf8')
        total_floor_pattern_str = r'(?<=\/)(\d+)(?=层)'.decode('utf8')
        floor_position_pattern_str = r'\W(?=区)'.decode('utf8')
        build_face_pattern_str = r'(?<=朝)(\W)'.decode('utf8')

        living_room = self.parse_helper(str, living_room_pattern_str)
        item['living_room_num'] = int(living_room)
        room_pattern = self.parse_helper(str, room_pattern_str)
        item['room_num'] = int(room_pattern)
        size = self.parse_helper(str, size_pattern_str)
        item['size'] = float(size)
        total_floor = self.parse_helper(str, total_floor_pattern_str)
        item['total_floor'] = int(total_floor) if total_floor is not None else None
        floor_position = self.parse_helper(str, floor_position_pattern_str)
        item['floor_position'] = floor_position
        build_face = self.parse_helper(str, build_face_pattern_str)
        item['build_face'] = build_face

    def parse_helper(self, str, pattern_str):
        p = re.compile(pattern_str)
        m = p.search(str)
        if m:
            return m.group()
        else:
            return None
