from analysis.bmap_dist_price import resolve_location
from lib.etl_util import compute_unit_price, load_dict_list_json
from datetime import date

file_name = "data/preowened-{}.json".format(date.today())
savefile = "data/location_price-{}.json".format(date.today())

if __name__ == '__main__':
    dict_list = load_dict_list_json(file_name)
    addr_price = compute_unit_price(dict_list)
    resolve_location(addr_price, savefile, max_jobs=3000)
