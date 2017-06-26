#! -*- encoding:utf-8 -*-
from multiprocessing import Lock

def locked_method(method):
    """Method decorator. Requires a lock object at self._lock"""
    def newmethod(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)
    return newmethod


class LockedSet(set):
    def __init__(self, *args, **kwargs):
        self._lock = Lock()
        super(LockedSet, self).__init__(*args, **kwargs)

    @locked_method
    def add(self,elem,  *args, **kwargs):
        return super(LockedSet, self).add(elem)

    @locked_method
    def remove(self,elem, *args, **kwargs):
        return super(LockedSet, self).remove(elem)

    @locked_method
    def __contains__(self, key):
        return super(LockedSet, self).__contains__(key)
