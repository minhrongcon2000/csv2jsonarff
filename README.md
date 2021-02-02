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
  [attribute 1's name]: {
    type: [attribute 1's type],
    labels?: [list of possible values]
  },
  ...
}
```

where attribute type follows the ARFF standard of weka. ``labels`` is only compulsory when an attribute is nominal. Read weka manual for more information.

## How to read JSON in Weka

Unfortunately, in some cases, the JSON format cannot be read by Weka Explorer, even though it can be read using Weka API. Hence, the only way to read the JSON file is via the API. Here is one example of reading JSON file using Weka API (suppose that you have setup your project properly with weka.jar as library file):

```Java
import weka.core.Instances;
import weka.core.converters.ConverterUtils;

public class Demo {
    public static void main(String[] args) throws Exception {
        Instances data = ConverterUtils.DataSource.read("/path/to/json_file.json");
        System.out.println(data);
    }
}

```

## TODO

Convert to JSON readable by Weka explorer
