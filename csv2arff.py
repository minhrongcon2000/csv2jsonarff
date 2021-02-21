import argparse
from utils import csv2arff, parse_args
import json
import shutil


# remove __pycache__ folder for better performance
shutil.rmtree("__pycache__")


src, dest, conf_path, relationname, delimiter = parse_args()

# load configuration file
with open(conf_path, "r") as f:
    print("Load config file...")
    config = json.load(f)

# save json file to specified path
with open(dest, "w") as f:
    csv2arff(src, dest, config, relationname=relationname, delimiter=delimiter)
