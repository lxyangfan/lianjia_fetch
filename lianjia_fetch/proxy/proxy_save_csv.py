# ! -*- encoding:utf8 -*-
import multiprocessing
import time, csv, re, requests
from bs4 import BeautifulSoup as Bs
from task_def import CrawTask

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def save_csv(file_name, set_var, mode='a'):
    with open(file_name, mode) as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(list(set_var))


def test_csv():
    vars = set(['hello', '10.123.123.123:80', '88.123.123.123:80']);
    with open('dt.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerow(list(vars))


def test_read_csv():
    with open('dt.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print row


class Consumer(multiprocessing.Process):
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
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
            print '%s: %s' % (proc_name, next_task)
            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class CrawTask(object):
    """ Craw proxy task"""

    def __init__(self, url):
        self.url = url
        self.proxies = set()

    def __call__(self):
        xx = requests.get(self.url, headers=headers)
        soup = Bs(xx.text, "lxml")
        ip_list = soup.find_all('tr', class_='odd')
        for item in ip_list:
            col_list = re.split(r'\s*', item.text)
            if col_list[4] == u'高匿':
                proxy = col_list[1] + ':' + col_list[2]
                self.proxies.add(proxy)
        return self

    def __str__(self):
        return 'Craw Url: %s  ' % (self.url)


def main():
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2
    print 'Creating %d consumers' % num_consumers
    consumers = [Consumer(tasks, results)
                 for i in xrange(num_consumers)]
    for w in consumers:
        w.start()

    # Enqueue jobs
    num_jobs = 5
    for i in xrange(1, num_jobs):
        url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        tasks.put(CrawTask(url))

    # Add a poison pill for each consumer, 开启几个进程就需要传递几个结束的消息
    for i in xrange(num_consumers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Start printing results
    while num_jobs:
        result = results.get()
        print 'Result:', result
        save_csv('dt.csv', result.proxies)
        num_jobs -= 1


if __name__ == '__main__':
    main()
    test_read_csv()
