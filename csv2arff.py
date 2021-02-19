import argparse
from utils import csv2arff
import json
import shutil


# remove __pycache__ folder for better performance
shutil.rmtree("__pycache__")

# generate help document
parser = argparse.ArgumentParser(
    description="Converting csv (with any delimiter) to json so that Weka can read"
)

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

# Exception handling with -i, -o, -conf compulsory flags
if src is None:
    raise Exception("Source file needs providing.")

if dest is None:
    raise Exception("Please provide json file name.")

if conf_path is None:
    raise Exception("Attribute configuration is needed.")

# load configuration file
with open(args.conf, "r") as f:
    print("Load config file...")
    config = json.load(f)

# save json file to specified path
with open(dest, "w") as f:
    csv2arff(src, dest, config, relationname=relationname, delimiter=delimiter)
