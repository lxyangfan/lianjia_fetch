#! -*- encoding:utf-8 -*-
"""
    使用百度GeoAPI, 解析json数据，查询地区和城镇地址，并转换成经纬度信息

"""

import requests
import json
import multiprocessing as MP
import csv
from datetime import date
from lianjia_fetch.proxy.mp_task_run import run_tasks
from lianjia_fetch.lib.etl_util import save_dict_list_json, load_dict_list_json
from lianjia_fetch.lib.url_util import url_encode_unicode

APP_key = "cvENTqYHfb5sLjXMQ4yWHKIPmx38ACs3"


class BaiduResolveLocation(object):
    """
        百度地图API解析地址 -> 经纬度
    """

    def __init__(self, position):
        self.position = position

    def __call__(self):
        try:
            url = u'http://api.map.baidu.com/geocoder/v2/?output=json&ret_coordtype=bd09ll&ak={0}&address={1}{2}{3}'.format(
                APP_key, url_encode_unicode(u"上海市"), url_encode_unicode(self.position["district"]),
                url_encode_unicode(self.position["town"]))
            print "访问URL: ", url
            resp = requests.get(url=url, timeout=5)
            if resp.status_code == 200:
                base = json.loads(resp.text)
                if base["status"] == 0:
                    location = base["result"]["location"]
                    self.position["lat"] = location["lat"]
                    self.position["lng"] = location["lng"]
                else:
                    self.position["lat"] = None
                    self.position["lng"] = None
                return self.position
            else:
                return None
        except RuntimeError, err:
            print "意外发生！", err
            return None


def load_data():
    return load_dict_list_json("../data/dt/dist_town_price-{}.json".format(date.today()))


def resolve_location():
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()
    task_postions = MP.Queue()

    list_v = load_data()
    for i in list_v:
        task_postions.put(i)

    num_jobs = 0
    max_num_jobs = 200
    while not task_postions.empty() and num_jobs <= max_num_jobs:
        position = task_postions.get()
        tasks.put(BaiduResolveLocation(position=position))
        num_jobs += 1

    run_tasks(tasks, results)

    print "任务结束..."

    dict_list = []
    while num_jobs:
        result = results.get()
        if result is not None:
            dict_list.append(result)
        num_jobs -= 1

    file_name = "../data/json/price_location-{}.json".format(date.today())
    save_dict_list_json(file_name, dict_list)
    print "保存文件结束..."


if __name__ == "__main__":
    # resolve_location()
    # po = {"district": u"上海浦东", "town": u"亮景路210号"}
    # po = {"district": u"浦东", "town": u"张江长泰广场"}
    po = {"district": u"静安区", "town": u"静安寺"}
    task = BaiduResolveLocation(po)
    res = task()
    for k, v in res.items():
        print k, v
