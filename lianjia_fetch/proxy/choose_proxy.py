#! -*- encoding:utf-8 -*-

import logging
from lib.file_util import read_csv_to_list
from task_def import VarifyProxyTask

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def choose_one_useful_proxy():
    proxies = []
    read_csv_to_list('useful.csv', proxies)
    for proxy in proxies:
        # print 'Proxy is {}'.format(proxy)
        logger.debug("chose proxy is %s", proxy)
        task = VarifyProxyTask(url=proxy, timeout=1)
        if task():
            return proxy
    return None



if __name__ == "__main__":
    proxy = choose_one_useful_proxy()
    if proxy:
        logger.debug("Find One useful proxy: %s", proxy)



