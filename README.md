# Genderize CSV

Python genderize.io script

#### Usage:
```sh
python genderize.py [required: input csv path] [required: output csv path] [optional: API_KEY]
```

#### Test usage:
```
python genderize.py test/test.csv test/out.csv
```

This script takes a single column CSV file with a header (first row says "name" or other) and feeds the names to genderize.io. It outputs a CSV file with the name, gender, probability, and count of every name.

#### Note:
- API_KEY (https://store.genderize.io) is required when requesting more than 1000 names a month
- genderize_nerrc.py is an older version of genderize.py. If you experience issues with the normal file, try this one, though it is not guaranteed to work and is missing features (feeding API key through command line, catching errors, etc.)

#### Requires:
Required module can be found in "dep" folder or pypi link (see "Dependencies")
```
pip install Genderize-0.1.5-py3-none-any.whl
```
Python 3.* (Known working: 3.6.1)


##### Dependencies:
- https://pypi.python.org/pypi/Genderize / https://github.com/SteelPangolin/genderize

#### Features:
- Bulk processing (tested with 100,000+ names).
- Estimates remaining time.
- Writes data after processing 10 names so little data is lost if genderize.io responds with a 502 error, network connection is lost, or request limit is reached.
- Support for genderize.io API key (allows processing of more than 1000 names /mo).

#### To-do:
- ~~Catch 502 bad gateway error and retry the request. Currently the program will just catch the error, print it, and exit.~~
- Add ability to search multi-column CSV file for column with specific header.
- Add support for optionally caching gender responses and searching through them for identical names before asking genderize for the data. This would lower API key request usage.
- Add better command line flags

#### "Chunks" explanation:
The Python Genderize client used limits requests to 10 names. To work around this, the code breaks the list of names down into chunks of 10. This approach also has the benefit of preventing data loss in case of a crash/server error as the results are written to the output file every 10 names.
