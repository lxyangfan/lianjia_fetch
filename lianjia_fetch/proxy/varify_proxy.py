# ! -*- encoding:utf8 -*-
import multiprocessing as MP
import time

from mp_task_run import run_tasks
from task_def import CrawTask, VarifyProxyTask


def fetch_proxies(page_num=2, save_file='new_proxy'):
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()

    # Enqueue jobs
    num_jobs = page_num
    for i in xrange(num_jobs):
        url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        tasks.put(CrawTask(url))

    run_tasks(tasks, results)

    while num_jobs:
        result = results.get()
        file_name = '{1}_{2}.csv'.format(save_file, time.strftime("%Y/%m/%d-%H:%I:%S", time.localtime()))
        save_csv(file_name, list(result))
        num_jobs -= 1


def varify_proxies(read_file='dt.csv', save_file='useful.csv'):
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()
    proxy_queue = MP.Queue()

    read_csv_to_queue(read_file, proxy_queue)

    num_jobs = 0
    max_num_jobs = 1000
    while not proxy_queue.empty() and num_jobs <= max_num_jobs:
        proxy = proxy_queue.get()
        tasks.put(VarifyProxyTask(proxy, timeout=1))
        num_jobs += 1

    run_tasks(tasks, results)

    final_proxy = []
    while num_jobs:
        result = results.get()
        if result is not None:
            final_proxy.append(result)
        num_jobs -= 1
    # save the useful
    save_csv(save_file, final_proxy, mode='a')


if __name__ == '__main__':
    varify_proxies()
