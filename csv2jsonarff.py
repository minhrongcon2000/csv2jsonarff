import argparse
from utils import csv2arffjson
import json
import shutil

shutil.rmtree("__pycache__")

parser = argparse.ArgumentParser(
    description="Converting csv (with any delimiter) to json so that Weka can read"
)

parser.add_argument("-i", help="path to csv file")
parser.add_argument("-o", help="path to output json file")
parser.add_argument(
    "-conf", help="a json file containing attribute configuration")
parser.add_argument(
    "-rname", help="Optional. Name of relation you want to store")
args = parser.parse_args()

src = args.i
dest = args.o
conf_path = args.conf

if src is None:
    raise Exception("Source file needs providing.")

if dest is None:
    raise Exception("Please provide json file name.")

if conf_path is None:
    raise Exception("Attribute configuration is needed.")

with open(args.conf, "r") as f:
    print("Load config file...")
    config = json.load(f)

with open(dest, "w") as f:
    print("Saving to json...")
    json.dump(csv2arffjson(
        src, config, relationname=args.rname if args.rname is not None else 'wekadata'), f, indent=4)
