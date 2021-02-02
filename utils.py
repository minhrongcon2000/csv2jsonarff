import json
from tqdm import tqdm
import mmap


def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


def getHeaderObj(relationname, attribute_conf):
    print("Generating header...")

    def getAttrObj(attr_info):
        attr_name, attr_type = attr_info
        return {
            "name": attr_name,
            "type": attr_type,
            "class": False,
            "weight": 1.0
        }
    return {
        "relation": relationname,
        "attributes": list(map(getAttrObj, attribute_conf.items()))
    }


def formatData(path, delimiter=','):
    print("format dataset...")
    data = []
    with open(path, 'r') as f:
        for line in tqdm(f, total=get_num_lines(path)):
            values = line.strip().split(delimiter)
            data.append({
                "sparse": False,
                "weight": 1.0,
                "values": values
            })
        f.close()
    return data


def csv2arffjson(path, attr_conf, relationname='wekadata', delimiter=','):
    return {
        "header": getHeaderObj(relationname, attr_conf),
        "data": formatData(path)
    }
