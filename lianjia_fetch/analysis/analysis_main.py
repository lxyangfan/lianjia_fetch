#! -*- encoding:utf-8 -*-
import requests
import json
import multiprocessing as MP
import csv
from datetime import date
from proxy.mp_task_run import run_tasks
from lib.etl_util import save_dict_list_in_csv

proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}


class ResolveLocation(object):
    def __init__(self, position):
        self.position = position

    def __call__(self):
        try:
            url = u'http://maps.google.com/maps/api/geocode/json?address=上海市{0}{1}&language=zh-CN&sensor=false'.format(
            self.position["district"], self.position["town"])
            print "访问URL: ", url
            resp = requests.get(url=url, proxies=proxies, timeout=5)
            if resp.status_code == 200:
                base = json.loads(resp.text)
                if len(base["results"]) > 0:
                    location = base["results"][0]["geometry"]["location"]
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

    def fetch_google_location(self):
        url = r'http://maps.google.com/maps/api/geocode/json?address=上海市{0}{1}&language=zh-CN&sensor=false'.format(
            self.position["district"], self.position["town"])
        print "访问URL: ", url
        resp = requests.get(url=url, proxies=proxies, timeout=5)
        if resp.status_code == 200:
            base = json.loads(resp.text)
            location = base["results"][0]["geometry"]["location"]
            self.position["lat"] = location["lat"]
            self.position["lng"] = location["lng"]
            return self.position
        else:
            print "失败！"


def load_data(list_v=None):
    if list_v is None:
        list_v = []
    with open("dist_town_df.csv", mode="r") as csvfile:
        rows = csv.reader(csvfile)
        for row in rows:
            if row[2] != 'town':
                item = {}
                item["district"] = unicode(row[1], "utf-8")
                item["town"] = unicode(row[2], "utf-8")
                item["unit_price"] = row[3]
                list_v.append(item)
    return list_v


def resove_location():
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
        tasks.put(ResolveLocation(position=position))
        num_jobs += 1

    run_tasks(tasks, results)

    dict_list = []
    while num_jobs:
        result = results.get()
        if result is not None:
            dict_list.append(result)
        num_jobs -= 1

    file_name = "price_location-{}.csv".format(date.today())
    save_dict_list_in_csv(file_name, dict_list)


if __name__ == "__main__":
    resove_location()
