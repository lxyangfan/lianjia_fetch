# -*- encoding:utf-8 -*-
from lib.etl_util import save_props_without_key
from proxy.lib.file_util import read_csv_to_list, save_prop_csv

import random
import multiprocessing as MP
from proxy.mp_task_run import run_tasks
from proxy.task_def import CrawlLianjiaTask
from datetime import date


def get_proxies(proxies=None):
    if proxies is None:
        proxies = []
    read_csv_to_list(csv_file="useful627.csv", list_var=proxies)
    return proxies


def random_get_proxy():
    proxies = get_proxies()
    size = len(proxies)
    if size >= 1:
        ind = random.randint(0, size - 1)
        return proxies[ind]
    else:
        return None


def fetch_lianjia():
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()
    task_urls = MP.Queue()
    base_url = "http://sh.lianjia.com/ershoufang/d"
    for i in xrange(1, 101):
        task_urls.put("{}{}".format(base_url, i))

    num_jobs = 0
    max_num_jobs = 100
    while not task_urls.empty() and num_jobs <= max_num_jobs:
        url = task_urls.get()
        tasks.put(CrawlLianjiaTask(url=url, proxy_ip=None))
        num_jobs += 1

    run_tasks(tasks, results)

    while num_jobs:
        result = results.get()
        if result is not None:
            file_name = "../data/props-{}.csv".format(date.today())
            save_props_without_key(file_name, result, mode="a")
        num_jobs -= 1


if __name__ == '__main__':
    fetch_lianjia()
