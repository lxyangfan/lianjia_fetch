# -*- encoding:utf-8 -*-
import pandas as pd
from datetime import date
from lianjia_fetch.lib.etl_util import save_dict_list_in_csv, load_dict_list_json, save_dict_list_json

lv = load_dict_list_json("../data/dt/dist_town_price-2017-06-30.json")

for i in xrange(0, 4):
    for k,v in lv[i].items():
        lv[i][k] = u"shit-{}".format(v)
        print k, v

save_dict_list_json("xx.json", lv)



