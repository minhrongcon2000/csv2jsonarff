# csv2jsonarff

Converting a csv file to json file (arff-like format) for Weka I/O. More about Weka at <https://www.cs.waikato.ac.nz/~ml/weka/>

## Motivation

Weka is a Machine Learning library written in Java whose goal is mainly for research. Hence, it is still in use by most university around the world. Despite having a variety of ML algorithm, Weka can only function normally with ARFF (whose delimiter is only comma) and some restricted use case of other file format, including the popular csv and JSON. Hence, the author of this repo wants to write a python script capable of transforming csv into appropriate JSON file readable to Weka. 

## Dependencies

- tqdm

## Usage

- Clone this repo
- Install tqdm via pip
- Run the following command:

```bash
python3 csv2jsonarff.py -i <input csv file> -o <output json filename> -conf <configuration file path>
```

_Note:_ Configuration file is a json file with following format.

```JSON
{
  "[attribute 1's name]": {
    "type": ["attribute 1's type"],
    "labels"?: ["list of possible values"]
  },
  ...
}
```

where attribute type follows the ARFF standard of weka. ``labels`` is optional and only compulsory when an attribute is nominal. Read weka manual for more information.

For example, suppose we want to predict whether a person has diabetes based on their weight and suppose further that we collected our dataset with two attributes: weight and status, in which 1 corresponds to having diabetes and 0 corresponds to reverse case. Then the attribute configuration file should be as follow:

```JSON
{
  "weight": {
    "type": "numeric"
  },
  "status": {
    "type": "nominal",
    "labes": ["0", "1"]
  }
}
```
