from proxy_pool import ProxyPool

if __name__ == '__main__':
    pool = ProxyPool()
    proxy = pool.getproxy()
    print proxy