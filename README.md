# csv2jsonarff

Converting a csv file to json file (arff-like format) for Weka I/O. More about Weka at <https://www.cs.waikato.ac.nz/~ml/weka/>

## Motivation

Weka is a Machine Learning library written in Java whose goal is mainly for research. Hence, it is still in use by most university around the world. Despite having a variety of ML algorithm, Weka can only function normally with ARFF (whose delimiter is only comma) and some restricted use case of other file format, including the popular csv and JSON. Hence, the author of this repo wants to write a python script capable of transforming csv into appropriate JSON file readable to Weka. 

## Dependencies

- tqdm

## Usage

TL;DR, do the following four steps:

1. Clone this repo
2. Install tqdm via pip (just for nice progress bar visualization xD)
3. Create attribute configuration file (must-have, read further to know how to create)
4. Run the following command:

```bash
python3 csv2jsonarff.py -i /path/to/csv_file.csv -o /path/to/output_json_file.json -conf /path/to/attr_config.json
```

### How to make attribute configuration file

Attribute configuration file is a json file that describes the type of each attributes. The file is needed since Java is a strongly-typed programming language, so every attribute needs to be clearly declared. The file should have the following format

```JSON
{
  "[attribute 1's name]": {
    "type": "attribute 1's type",
    "labels"?: ["list of possible values"]
  },
  ...
}
```

where attribute type follows the ARFF standard of weka. 

Following is the description of each ARFF types.

| ARFF type | Description                                                                                 |
|-----------|---------------------------------------------------------------------------------------------|
| numeric   | comparable datatype, usually relevant to float, and int type in other programming languages |
| nominal   | non-comparable datatype, usually has a certain number of possible values                    |
| string    | relevant to string type in other programming language                                       |
| datetime  | should be in the form of 'yyyy-mm-dd hh:mm:ss'                                              |

Noticing that in the attribute configuration file, there is a ``labels`` attribute with the question mark following this. This indicates that the attribute is optional. However, there is one scenario that the attribute is compulsory; that is the case of nominal attribute. As defined, nominal attribute only accepts a certain number of values. For example, a patient can either have diabete or not have diabete, and a fruit can only be orange, apple, or banana (if your dataset has more types of fruits, then the number of possible values will be greater but that number is finite). 

To give an illustration on how to create an attribute configuration file, suppose we want to predict whether a person has diabetes based on their weight and suppose further that we collected a dataset with two attributes: weight and status, in which 1 corresponds to having diabetes and 0 corresponds to reverse case. Then the attribute configuration file should be as follow:

```JSON
{
  "weight": {
    "type": "numeric"
  },
  "status": {
    "type": "nominal",
    "labels": [
      "0", 
      "1"
    ]
  }
}
```
