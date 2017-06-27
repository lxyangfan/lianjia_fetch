#coding:utf8
import csv

from proxy.lib.file_util import save_dict_csv

data = [{"addr":u"上海", "position":u"朝向北"}, {"addr":u"上海", "position":u"朝向南nan"}]

save_dict_csv("good.csv", list_var=data)

# def test():
#     with open('results.csv','wb') as f:
#         f.write(u'\ufeff'.encode('utf8'))
#         for row in data:
#             for key,value in sorted(row.items()):
#                 f.write(str(key) + ':' + str(value) + "\t")
#             f.write("\n")
