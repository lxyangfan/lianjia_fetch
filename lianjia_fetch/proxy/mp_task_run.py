# ! -*- encoding:utf8 -*-
import multiprocessing as MP
import time, csv, re
import logging
import os
import time
from logging.config import fileConfig

fileConfig("log_util/log_conf.ini")
logger = logging.getLogger("mpTaskRunLog")

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,fr-FR;q=0.6,fr;q=0.4,en-US;q=0.2,en;q=0.2',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


class Consumer(MP.Process):
    def __init__(self, task_queue, result_queue):
        MP.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        try:
            while True:
                next_task = self.task_queue.get()
                if next_task is None:
                    # Poison pill means shutdown
                    print '%s: Exiting' % proc_name
                    self.task_queue.task_done()
                    return
                # print '%s: %s' % (proc_name, next_task)
                answer = next_task()
                self.task_queue.task_done()
                self.result_queue.put(answer)
                time.sleep(0.01)  # Just enough to let the Queue finish
        except RuntimeError, err:
            # TODO handle with err
            logger.error("工作进程出错", err)
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
