# Genderize CSV

**Python genderize.io script**

This script takes a single column CSV file with a header and feeds the names to genderize.io. It outputs a CSV file with the name, gender, probability, and count of every name.

### Usage:
```sh
python genderize.py [-h] -i INPUT -o OUTPUT [-k KEY] [-c] [-ns] [-nh]
```

```
optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     API key
  -c, --catch           Try to gracefully handle server 502 errors
  -nh, --noheader       Input has no header row

required arguments:
  -i INPUT, --input INPUT
                        Input file name
  -o OUTPUT, --output OUTPUT
                        Output file name
```

### Beta usage:
```
genderize_beta.py [-h] -i INPUT -o OUTPUT [-k KEY] [-c] [-a] [-nh]
```

```
optional arguments:
  -h, --help            show this help message and exit
  -k KEY, --key KEY     API key
  -c, --catch           Try to gracefully handle server 502 errors
  -a, --auto            Automatically complete gender for identical names
  -nh, --noheader       Input has no header row

required arguments:
  -i INPUT, --input INPUT
                        Input file name
  -o OUTPUT, --output OUTPUT
                        Output file name
```

#### Beta features:
- Auto flag: Only requests unique names from genderize.io, autocompletes the rest. May significantly lower API key usage.

### Test usage:
```
python genderize.py -i test/test.csv -o test/out.csv --catch
```

### Note:
- API key (https://store.genderize.io) is required when requesting more than 1000 names a month.
- genderize_beta.py may be unstable and is meant for developing and testing new features.

### Requires:
Required module can be found in "dep" folder or pypi link (see "Dependencies")
```
pip install Genderize-0.1.5-py3-none-any.whl
```
Python 3.* (Known working: 3.6.1)

#### Dependencies:
- https://pypi.python.org/pypi/Genderize / https://github.com/SteelPangolin/genderize

### Features:
- Bulk processing (tested with 100,000+ names).
- Estimates remaining time.
- Writes data after processing 10 names so little data is lost if genderize.io responds with a 502 error, network connection is lost, or request limit is reached.
- Support for genderize.io API key (allows processing of more than 1000 names /mo).

### To-do:
- Add ability to search multi-column CSV file for column with specific header.
- Add support for alternate output formats.
- Add support for using file as a module.
- ~~Add support for optionally caching gender responses and searching through them for identical names before asking genderize for the data. This would lower API key request usage.~~ BETA
- ~~Catch 502 bad gateway error and retry the request. Currently the program will just catch the error, print it, and exit.~~ DONE
- ~~Add better command line flags~~ DONE


#### "Chunks" explanation:
The Python Genderize client used limits requests to 10 names. To work around this, the code breaks the list of names down into chunks of 10. This approach also has the benefit of preventing data loss in case of a crash/server error as the results are written to the output file every 10 names.
