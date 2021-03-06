import json
from tqdm import tqdm
import mmap
import re
import argparse


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
                    'Inconsistency detected between data and attribute config: {} != {}'.format(len(line.split(delimiter)), len(attribute_conf)))


# code for converting csv to json
# =====================================================================
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
        attr_obj = {
            "name": attr_info['name'],
            "type": attr_info["type"],
            "class": False,
            "weight": 1.0
        }

        if attr_info['type'] == 'nominal':
            attr_obj['labels'] = attr_info['labels']
        return attr_obj

    return {
        "relation": relationname,
        "attributes": list(map(getAttrObj, attribute_conf))
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
# =====================================================================

# code for converting csv to json
# =====================================================================


def processed_string_data(sentence):
    """replace " with '

    Args:
        sentence (str): string of characters

    Returns:
        str: original string put in "" with all internal " replaced with '
    """
    return '"{}"'.format(re.sub("\"", "'", sentence))


def csv2arff(src, dest, attr_conf, relationname='wekadata', delimiter=','):
    """convert csv to arff

    Args:
        src (str): path to csv source file
        dest (str): path to store designated arff file
        attr_conf (str): path to configuration file
        relationname (str, optional): name of relation. Defaults to 'wekadata'.
        delimiter (str, optional): field delimiter. Defaults to ','.
    """
    # check consistency between config file and csv file
    isDataAttributeConsistent(attr_conf, src, delimiter=delimiter)

    with open(dest, "w") as output_file:
        # writing header of arff file
        print("Writing header...")

        output_file.write("@relation {}\n\n".format(relationname))

        for attr_info in tqdm(attr_conf):
            if attr_info["type"] != "nominal":
                output_file.write(
                    f'@attribute {attr_info["name"]} {attr_info["type"]}\n')
            else:
                label_output = str(attr_info["labels"]).replace(
                    '[', '{').replace(']', '}')
                output_file.write(
                    f'@attribute {attr_info["name"]} {label_output}\n')

        # writing actual data of arff file
        output_file.write('\n@data\n')
        with open(src, "r") as input_file:
            print("Writing data...")
            for line in tqdm(input_file, total=get_num_lines(src)):
                instance = line.strip().split(delimiter)
                for i in range(len(instance)):
                    if attr_conf[i]["type"] == 'string':
                        instance[i] = processed_string_data(instance[i])
                output_file.write(','.join(map(str, instance)))
                output_file.write('\n')


def parse_args():
    # Load input-special-character converter
    input2special_char = json.load(open("input2special_char.json", "r"))

    parser = argparse.ArgumentParser(
        description="Converting csv (with any delimiter) to json so that Weka can read")

    # arguments and documents
    parser.add_argument("-i", help="path to csv file")
    parser.add_argument("-o", help="path to output json file")
    parser.add_argument(
        "-conf", help="a json file containing attribute configuration")
    parser.add_argument(
        "-rname", help="Optional. Name of relation you want to store. Default to wekadata")
    parser.add_argument(
        "-delim",
        help="Optional. Delimiter of csv file. Default to ,"
    )

    # get input from argument flags
    args = parser.parse_args()

    # retrieve path to csv file, output json file, configuration file, dataset's name, and delimiter
    src = args.i
    dest = args.o
    conf_path = args.conf
    relationname = args.rname if args.rname is not None else 'wekadata'
    delimiter = args.delim if args.delim is not None else ','

    if src is None:
        raise Exception("Source file needs providing.")

    if dest is None:
        raise Exception("Please provide json file name.")

    if conf_path is None:
        raise Exception("Attribute configuration is needed.")

    if delimiter not in input2special_char:
        raise Exception(
            "Delimiter not supported, please add it to input2special_character.json")

    return src, dest, conf_path, relationname, input2special_char[delimiter]
