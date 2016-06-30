"""
This script exports the default compartments from openLCA to a file that can
be directly used as compartment mapping file in the iomb package.

Note that this script should be executed within openLCA.
"""

import codecs
import csv
import org.openlca.core.model.ModelType as MT

# set this path to the file where the compartments should be written
EXPORT_PATH = 'C:/Users/Besitzer/Desktop/compartment_meta_data.csv'


def main():
    global olca
    entries = []
    fn = make_collector(entries)
    olca.eachCategory(fn)
    entries.sort(key=lambda x: (x[0] + x[1]).lower())
    with codecs.open(EXPORT_PATH, 'w', 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Compartment', 'Sub-Compartment', 'UUID', 'Direction'])
        for e in entries:
            writer.writerow(e)


def make_collector(entries):
    """ Creates a function that collects the compartments data from openLCA. """

    def fn(category):
        if category.getModelType() != MT.FLOW:
            return
        parent = category.getCategory()
        if parent is None or parent.getName() == 'Elementary flows':
            return
        direction = 'input' if parent.getName() == 'resource' else 'output'
        entry = [parent.getName(), category.getName(), category.getRefId(),
                 direction]
        entries.append(entry)

    return fn


if __name__ == '__main__':
    main()
