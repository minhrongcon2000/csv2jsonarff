# csv2jsonarff
Converting a csv file to json file (arff-like format) for Weka I/O. More about Weka at https://www.cs.waikato.ac.nz/~ml/weka/

## Dependencies
* tqdm

## Usage
* Clone this repo
* Install tqdm via pip
* Run the following command: 
```bash
python3 csv2jsonarff.py -i <input csv file> -o <output json filename> -conf <configuration file path>
```
*Note:* Configuration file is a json file with following format.
```
{
  [attribute 1's name]: [attribute 1's type],
  ...
}
```
where attribute type follows the ARFF standard of weka. Read weka manual for more information.

### How to read JSON in Weka

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

After doing that, you can use Weka API to convert back into ARFF, which is readable by weka explorer.
