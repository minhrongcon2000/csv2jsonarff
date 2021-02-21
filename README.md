# csv2jsonarff

Converting a csv file to json file (arff-like format) for Weka I/O. More about Weka at <https://www.cs.waikato.ac.nz/~ml/weka/>

## Motivation

Weka is a Machine Learning library written in Java whose goal is mainly for research. Hence, it is still in use by most university around the world. Despite having a variety of ML algorithm, Weka can only function normally with ARFF (whose delimiter is only comma) and some restricted use case of other file format, including the popular csv and JSON. Hence, the author of this repo wants to write scripts to convert other file types to ARFF.

## Dependencies

- tqdm

## Usage

TL;DR, do the following four steps:

1. Clone this repo
2. Install tqdm via pip (just for nice progress bar visualization xD)
3. Create attribute configuration file (must-have, read further to know how to create)
4. Choose methods that you want. Conversion methods are always in the form of ``<src>2<dest>.py``. For example, file ``csv2arff.py`` will convert csv to arff file.
5. Run the desire file. For example, in the case of csv2arff.py, the command should be

```bash
python3 csv2jsonarff.py -i /path/to/csv_file.csv -o /path/to/output_json_file.json -conf /path/to/attr_config.json -delim 'field_delimiter'
```

Every methods is guaranteed to have the same types of flags. Those flags are

```bash
python3 csv2arff.py -h 
usage: csv2arff.py [-h] [-i I] [-o O] [-conf CONF] [-rname RNAME]
                   [-delim DELIM]

Converting csv (with any delimiter) to json so that Weka can read

optional arguments:
  -h, --help    show this help message and exit
  -i I          path to csv file
  -o O          path to output json file
  -conf CONF    a json file containing attribute configuration
  -rname RNAME  Optional. Name of relation you want to store. Default to
                wekadata
  -delim DELIM  Optional. Delimiter of csv file. Default to ,
```

Please remember that for delimiter, always put it between two quotation marks. We know that delimiter can also be updated, so we allow developers to add more delimiter into ``input2special_char.json``, whose keys are user's possible inputs and values are corresponding special character in Python.

For how to make configuration file, please check the next section.

### How to make attribute configuration file

Attribute configuration file is a JSON file that describes attributes. The file is needed since Java is a strongly-typed programming language, so every attribute needs to be clearly declared. The file should have the following format

```JSON
[
  {
    "name": "[attribute 1's name]",
    "type": "attribute 1's type",
    "labels": ["list of possible values"]
  },
  {
    "name": "[attribute 2's name]",
    "type": "attribute 2's type",
    "labels": ["list of possible values"]
  },
  ...
]
```

where attribute type follows the ARFF standard of weka. Field ``labels`` is optional and only compulsory for attribute with nominal type.

Following is the description of each ARFF types.

| ARFF type | Description                                                                                 |
|-----------|---------------------------------------------------------------------------------------------|
| numeric   | comparable datatype, usually relevant to float, and int type in other programming languages |
| nominal   | non-comparable datatype, usually has a certain number of possible values                    |
| string    | relevant to string type in other programming language                                       |
| datetime  | should be in the form of 'yyyy-mm-dd hh:mm:ss'                                              |

To give an illustration on how to create an attribute configuration file, suppose we want to predict whether a person has diabetes based on their weight and suppose further that we collected a dataset with two attributes: weight and status, in which 1 corresponds to having diabetes and 0 corresponds to reverse case. Then the attribute configuration file should be as follow:

```JSON
[
  {
    "name": "weight",
    "type": "float"
  },
  {
    "name": "status", 
    "type": "nominal",
    "labels": [0, 1]
  }
]
```
