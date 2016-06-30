"""
This script exports the default locations from openLCA to a file that can
be directly used as location mapping file in the iomb package.

Note that this script should be executed within openLCA.
"""

import codecs
import csv

# set this path to the file where the locations should be written
EXPORT_PATH = 'C:/Users/Besitzer/Desktop/location_meta_data.csv'


def main():
    global olca
    entries = []
    fn = make_collector(entries)
    olca.eachLocation(fn)
    entries.sort(key=lambda x: x[0].lower())
    with codecs.open(EXPORT_PATH, 'w', 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Location-Code', 'Location-Name', 'Location-UUID'])
        for e in entries:
            writer.writerow(e)


def make_collector(entries):
    """ Creates a function that collects the location data from openLCA. """

    def fn(loc):
        entry = [loc.getCode(), loc.getName(), loc.getRefId()]
        entries.append(entry)

    return fn


if __name__ == '__main__':
    main()
