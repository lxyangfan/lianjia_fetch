# ! -*- encoding:utf8 -*-
import multiprocessing as MP
from multiprocessing import Manager, Queue, Value, Lock
from proxy_pool import GatherProxy
import time


def task(url, v):
    print 'Url is:', url
    v.value += 1
    return url


def apply_pool_test():
    url = 'http://sh.lianjia.com/d'
    useful_proxy_num = Value('i', 0)


    pool_size = MP.cpu_count() * 2
    print 'Pool count', pool_size
    # init process pool
    pool = MP.Pool(processes=pool_size)
    # mark the start time
    start_time = time.time()
    # task num is 100, and thread num is 8
    for i in xrange(100):
        pool.apply_async(task, ('{0}{1}'.format(url, i),useful_proxy_num,))

    pool.close()
    pool.join()
    # computing elapsed time
    end_time = time.time()
    print 'Time used: {0}'.format(end_time - start_time)
    print 'Useful proxy num, ', useful_proxy_num.value


def pool_map_test():
    urls = [
        'https://www.baidu.com',
        'http://www.meituan.com/',
        'http://blog.csdn.net/',
        'http://xxxyxxx.net'
    ]

    print 'Cpu count', MP.cpu_count()
    pool_size = MP.cpu_count() * 2
    print 'Pool count', pool_size
    pool = MP.Pool(processes=pool_size)

    pool_outputs = pool.map(task, urls)
    pool.close()
    pool.join()

    print 'Pool  :', pool_outputs


if __name__ == '__main__':
    apply_pool_test()