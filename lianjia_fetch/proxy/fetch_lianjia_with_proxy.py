from lib.file_util import read_csv_to_list, save_prop_csv
import random
import multiprocessing as MP
from mp_task_run import run_tasks
from task_def import CrawlLianjiaTask
from proxy_save_csv import save_csv
from lib.file_util import read_csv_to_queue


def get_proxies(proxies=None):
    if proxies is None:
        proxies = []
    read_csv_to_list(csv_file="useful627.csv", list_var=proxies)
    return proxies


def random_get_proxy():
    proxies = get_proxies()
    size = len(proxies)
    if size >= 1:
        ind = random.randint(0, size-1)
        return proxies[ind]
    else:
        return None


def main():
    threads = []


def fetch_lianjia():
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()
    task_urls = MP.Queue()
    base_url = "http://sh.lianjia.com/ershoufang/"
    for i in xrange(1, 100):
        task_urls.put("{}{}".format(base_url, i))

    num_jobs = 0
    max_num_jobs = 100
    while not task_urls.empty() and num_jobs <= max_num_jobs:
        url = task_urls.get()
        proxy = random_get_proxy()
        tasks.put(CrawlLianjiaTask(url=url, proxy_ip=None))
        num_jobs += 1

    run_tasks(tasks, results)

    while num_jobs:
        result = results.get()
        if result is not None:
            save_prop_csv("pros-0627.csv", result, mode="a")
        num_jobs -= 1


if __name__ == '__main__':
    fetch_lianjia()
