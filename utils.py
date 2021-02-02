import json
from tqdm import tqdm
import mmap


def get_num_lines(file_path):
    """get the number of data point in the csv file

    Args:
        file_path (string): path to a csv file

    Returns:
        int: number of lines in csv file
    """
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


def isDataAttributeConsistent(attribute_conf, input_path, delimiter=','):
    """check if attribute configuration has the same number of attribute as the csv dataset

    Args:
        attribute_conf (dict): attribute configuration loaded from file
        input_path (string): path to csv file
        delimiter (string, optional): delimiter of csv file. Defaults to ','.

    Raises:
        Exception: raised if the number of attribute in configuration is different from that number in dataset
    """
    with open(input_path, "r") as f:
        for line in f:
            if len(line.split(delimiter)) != len(attribute_conf):
                raise Exception(
                    'Inconsistency detected between data and attribute config')


def getHeaderObj(relationname, attribute_conf):
    """Generate header of ARFF file in JSON format

    Args:
        relationname (string): relation name, can be understood as name of dataset
        attribute_conf (dict): attribute configuration load from file

    Returns:
        dict: header JSON object of ARFF format
    """
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
    """format dataset in the form of ARFF-like JSON

    Args:
        path (string): path to csv file. Attribute names should be deleted
        delimiter (string, optional): delimiter of csv file. Defaults to ','.

    Returns:
        list: list of JSON object representing each instance in dataset
    """
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
    """convert csv to json that weka can read

    Args:
        path (string): path to csv file
        attr_conf (string): attribute configuration loaded from file 
        relationname (string, optional): name of dataset. Defaults to 'wekadata'.
        delimiter (string, optional): delimiter of csv fil. Defaults to ','.

    Returns:
        dict: JSON format of csv file that weka can read
    """
    isDataAttributeConsistent(attr_conf, path, delimiter=delimiter)
    return {
        "header": getHeaderObj(relationname, attr_conf),
        "data": formatData(path, delimiter)
    }
