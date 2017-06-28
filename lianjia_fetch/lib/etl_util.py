#! -*- encoding:utf-8 -*-
import csv
import re


def save_props(file_name, list_var, mode='wb'):
    with open(file_name, mode) as f:
        for row in list_var:
            for key, value in sorted(row.items()):
                f.write(str(key) + ':')
                if type(value) == unicode:
                    f.write("{},".format(str(value.encode("utf-8"))))
                else:
                    f.write("{},".format(value))
            f.write("\n")


def save_props_without_key(file_name, list_var, mode='wb'):
    with open(file_name, mode) as f:
        for row in list_var:
            for key, value in sorted(row.items()):
                if type(value) == unicode:
                    f.write("{},".format(str(value.encode("utf-8"))))
                else:
                    f.write("{},".format(value))
            f.write("\n")


def load_pros(file_name, list_var=None):
    if list_var is None:
        list_var = []

    with open(file_name, "r") as f:
        list_of_lines = f.readlines()
        for line in list_of_lines:
            dic = line_to_dict(line)
            if dic:
                list_var.append(dic)
    return list_var


def line_to_dict(line):
    """
        一行逗号分隔的key-value转为dict
        如
        'k1:v1,k2:v2,k3:v3,' => {"k1":v1,"k2":v2,"k3":v3}
    """
    if line[-1:] == ",":
        line = line[:-1]
    raw_kv_list = re.split(",", line)

    pat1 = r'.*(?=:)'
    pat2 = r'(?<=:).*'
    p1 = re.compile(pat1)
    p2 = re.compile(pat2)

    if raw_kv_list is not None and len(raw_kv_list) > 0:
        dic = {}
        for kv in raw_kv_list:
            m1 = p1.search(kv)
            m2 = p2.search(kv)
            if m1:
                dic[m1.group()] = m2.group() if m2 else None
        return dic

    return None


def save_dict_list_in_csv(file_name, dict_list=None):
    with open(file_name, mode="w") as csvfile:
        fwriter = csv.writer(csvfile)
        for item in dict_list:
            list_v = []
            for k,v in sorted(item.items()):
                if type(v) == unicode:
                    list_v.append(v.encode("utf-8"))
                else:
                    list_v.append(v)
            fwriter.writerow(list_v)



if __name__ == "__main__":
    lv = load_pros("../data/pros-0627.csv")
    save_props_without_key("../data/props.csv", lv)
