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


def isDataAttributeConsistent(attribute_conf, input_path, delimiter=','):
    with open(input_path, "r") as f:
        for line in f:
            if len(line.split(delimiter)) != len(attribute_conf):
                raise Exception(
                    'Inconsistency detected between data and attribute config')


def getHeaderObj(relationname, attribute_conf):
    print("Generating header...")

    def getAttrObj(attr_info):
        attr_name, attr_type = attr_info
        attr_obj = {
            "name": attr_name,
            "type": attr_type["type"],
            "class": False,
            "weight": 1.0
        }

        if attr_type['type'] == 'nominal':
            attr_obj['labels'] = attr_type['labels']
        return attr_obj

    return {
        "relation": relationname,
        "attributes": list(map(getAttrObj, attribute_conf.items()))
    }


def formatData(path, delimiter=','):
    print("Format dataset...")
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
    isDataAttributeConsistent(attr_conf, path, delimiter=delimiter)
    return {
        "header": getHeaderObj(relationname, attr_conf),
        "data": formatData(path, delimiter)
    }
