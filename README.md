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
