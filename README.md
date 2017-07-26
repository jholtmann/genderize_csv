# Genderize Python
Python genderize.io script

```sh
python genderize.py [input csv] [output csv]
```

This script takes a single column CSV file with a header (first row says "name" or other) and feeds the names to genderize.io. It outputs a CSV file with the name, gender, probability, and count of every name.

##### Features:
- Bulk processing (tested up to 100,000 names).
- Estimates remaining time.
- Writes data after processing 10 names so little data is lost if genderize.io responds with a 502 error, network connection is lost, or request limit is reached.
- Support for genderize.io API key (allows processing of more than 1000 names /mo).

#### Dependencies:
- https://pypi.python.org/pypi/Genderize (https://github.com/SteelPangolin/genderize)

#### To-do:
- ~~Catch 502 bad gateway error and retry the request. Currently the program will just catch the error, print it, and exit.~~ DONE (not tested thouroughly enough yet, so genderize_nerrc.py was added in case error catching causes problems)
- Add ability to search multi-column CSV file for column with specific header.
- Add support for optionally caching gender responses and searching through them for identical names before asking genderize for the data. This would lower API key request usage.

##### Note:
For some reason, the python genderize client used limits requests to 10 names. To work around this, the code breaks the names down into chunks of 10. This has the unintentional benefit of preventing data loss in case of a crash/server error as the results are written every 10 names. As such, it doesn't seem worth looking into why the 10 name request limit exists, as it is currenty also a feature.