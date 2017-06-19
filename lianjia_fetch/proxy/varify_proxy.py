# ! -*- encoding:utf8 -*-
import multiprocessing as MP
import time, csv, re
from task_def import CrawTask, VarifyProxyTask

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def save_csv(file_name, list_var, mode='a'):
    with open(file_name, mode) as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(list_var)


def test_csv():
    vars = set(['hello', '10.123.123.123:80', '88.123.123.123:80']);
    with open('dt.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(list(vars))


def test_read_csv():
    with open('dt.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row[0]


def read_csv_to_queue(csv_file, proxy_queue):
    if csv_file is None:
        csv_file = 'dt.csv'
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 1:
                proxy_queue.put(row[0])


class Consumer(MP.Process):
    def __init__(self, task_queue, result_queue):
        MP.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print '%s: Exiting' % proc_name
                self.task_queue.task_done()
                break
            #print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


def run_tasks(tasks_queue, results_queue):
    # Start consumers
    num_consumers = MP.cpu_count() * 2
    consumers = [Consumer(tasks_queue, results_queue)
                 for i in xrange(num_consumers)]
    for w in consumers:
        w.start()

    # Add a poison pill for each consumer, 开启几个进程就需要传递几个结束的消息
    for i in xrange(num_consumers):
        tasks_queue.put(None)

    # Wait for all of the tasks to finish
    tasks_queue.join()


def main():
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()

    # Enqueue jobs
    num_jobs = 2
    for i in xrange(num_jobs):
        url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        tasks.put(CrawTask(url))

    run_tasks(tasks, results)

    proxy_variy_tasks = MP.JoinableQueue()
    qualify_proxies = MP.Queue()

    while num_jobs:
        result = results.get()
        print 'Result:', result
        num_jobs -= 1


def varify_proxies(read_file='dt.csv', save_file='useful.csv'):
    # Establish communication queues
    tasks = MP.JoinableQueue()
    results = MP.Queue()
    proxy_queue = MP.Queue()

    read_csv_to_queue(read_file, proxy_queue)

    num_jobs = 0
    max_num_jobs = 500
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
    save_csv(save_file, final_proxy, mode='wb')


if __name__ == '__main__':
    varify_proxies('useful.csv', 'good.csv')
