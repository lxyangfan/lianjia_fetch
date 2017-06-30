# -*- encoding:utf-8 -*-
import pandas as pd
from datetime import date

names = ["addr", "build_face", "district", "floor_position","living_room_num","name","price","price_unit", "room_num","size","total_floor","town","year","unused" ]
props = pd.read_csv("../data/props-{}.csv".format(date.today()), index_col=False, names=names)


districts_props = props[["district","town", "price","size"]]
# 处理单价和文字（utf-8)
districts_props["unit_price"] = districts_props["price"] / districts_props["size"]
towns = [unicode(item, 'utf-8') for item in districts_props['town']]
districts = [unicode(item, 'utf-8') for item in districts_props['district']]
districts_props['town'] = towns
districts_props['district'] = districts

# group by 运算
dist_town = districts_props.groupby(["district","town"]).mean().reset_index()
dist_town_ordered = dist_town.sort_values(by="unit_price", ascending=False).reset_index()


dist_town_df = dist_town_ordered[["district", "town", "unit_price"]]

# 还挺优雅的
dist_town_df["district"] = dist_town_df["district"].apply(lambda s: u"浦东新区"  if s == u"浦东" else u"{}区".format(s))
dist_town_df.to_json("../data/dt/dist_town_price-{}.json".format(date.today()), orient="records")
