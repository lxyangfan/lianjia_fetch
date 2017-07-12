#!/usr/bin/python
#encoding:utf-8
from datetime import date
import time

with open("time.txt", "a") as cfile:
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\n"
    print time_str
    cfile.write(time_str)

