#encoding:utf-8

import re
import json

def fetch_position(line):
    ptn = r"(?<=POSITION:).*(?=\n)"
    cptn = re.compile(ptn)
    m = cptn.search(line)
    if m:
        line = m.group().replace("'", '"')
        line = line.replace('u"', '"')
        return line
    else:
        return None


def analyse_log(filename="info-log.log"):
    items = []
    with open(filename, "r") as logfile:
        lines = logfile.readlines()
        for line in lines:
            try:
                posi = fetch_position(line)
                if posi:
                    item = json.loads(posi, encoding="utf-8")
                    items.append(item)
            except ValueError, err:
                print err
            finally:
                pass
    return items


if __name__ == "__main__":
    items = analyse_log()
    print "解析后items大小，", len(items)
    with open("little.json", "w") as jfile:
        json.dump(items, jfile)

