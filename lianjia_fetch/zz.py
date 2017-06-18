#! -*- encoding:utf8 -*-
import re

def room():
    str = r"124 2室1厅".decode('utf8')
    print 'raw str', str
    p1_str = r'(\d+)(?=室)'.decode('utf8')
    p2_str = r'(?<=室)(\d+)(?=厅)'.decode('utf8')
    p3_str = r'(\d+)(?=室)(\d+)(?=厅)'.decode('utf8')
    print 'pattern', p2_str
#    p2 = re.compile(r'(?<=室).*(?=厅)'.decode('utf8'))
    p1 = re.compile(p1_str)
    p2 = re.compile(p2_str)
    p3 = re.compile(p3_str)
    m1_num = p1.search(str)
    m2_num = p2.search(str)
    m3_num = p3.search(str)
    if  m1_num:
        print m1_num.group(1)
    else:
        print "匹配失败"
    if  m2_num:
        print m2_num.group(1)
    else:
        print "匹配失败"
    if  m3_num:
        print m3_num.group(1)
    else:
        print "匹配失败"

def size():
    str = r'33.99平 48平'.decode('utf8')
    p_str = r'(\d+|\d+\.\d+)(?=平)'.decode('utf8')
    p = re.compile(p_str)
    m = p.findall(str)
    if m:
        print m
    else:
        print "匹配失败"

def floor():
    str = r'| 高区/6层 | '.decode('utf8')
    p_str = r'(?<=\/)(\d+)(?=层)'.decode('utf8')
    p = re.compile(p_str)
    m = p.search(str)
    if m:
        print m.group()
    else:
        print "匹配失败"

def floor_pos():
    str = r'| 高区/6层 | '.decode('utf8')
    p_str = r'\W(?=区)'.decode('utf8')
    p = re.compile(p_str)
    m = p.search(str)
    if m:
        print m.group()
    else:
        print "匹配失败"

def parse_prop_size_info(str, item):
    """解析房间大小和方位，比如： 1室1厅 | 57.5平 | 高区/6层 | 朝南
    """
    living_room_pattern_str = r'\d+(?=室)'.decode('utf8')
    room_pattern_str = r'(?<=室)\d+(?=厅)'.decode('utf8')
    size_pattern_str = r'(\d+|\d+\.\d+)(?=平)'.decode('utf8')
    total_floor_pattern_str = r'(?<=\/)(\d+)(?=层)'.decode('utf8')
    floor_position_pattern_str = r'\W(?=区)'.decode('utf8')
    build_face_pattern_str = r'(?<=朝)(\W)'.decode('utf8')

    living_room = parse_helper(str, living_room_pattern_str)
    item['living_room_num'] = int(living_room)
    room_pattern = parse_helper(str, room_pattern_str)
    item['room_num'] = int(room_pattern)
    size = parse_helper(str, size_pattern_str)
    item['size'] = float(size)
    total_floor = parse_helper(str, total_floor_pattern_str)
    item['total_floor'] = int(total_floor)
    floor_position = parse_helper(str, floor_position_pattern_str)
    item['floor_position'] = floor_position
    build_face = parse_helper(str, build_face_pattern_str)
    item['build_face'] = build_face


def parse_helper(str, pattern_str):
    p = re.compile(pattern_str)
    m = p.search(str)
    if m:
        return m.group()
    else:
        return None


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

    year_p_str = r'\d+(?=年)'.decode('utf8')
    m = re.search(year_p_str, list[3].encode("utf8"))
    if m:
        item.update({'year' : int(m.group())})
    else:
        item.update({'year' : None})
    return item

if __name__=="__main__":
    str =  """   东陆新村六街坊 | 浦东 | 金桥 | 1995年建
    """.decode('utf8')
    item = {}
    parse_prop_distric_and_year(str, item)
    print item