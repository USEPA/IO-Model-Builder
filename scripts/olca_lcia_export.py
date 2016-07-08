"""
This script exports an LCIA method from openLCA to a file that can be directly
used in the iomb package.

Note that this script should be executed within openLCA.
"""

import codecs
import csv

# set this path to the file where the method file should be written
EXPORT_PATH = 'C:/Users/Besitzer/Desktop/lcia_factors.csv'
METHOD_NAME = 'CML (baseline)'


def main():
    global olca
    method = olca.getMethod(METHOD_NAME)
    rows = []
    for category in method.getImpactCategories():
        for factor in category.getImpactFactors():
            flow = factor.getFlow()
            row = [method.getName(),
                   category.getName(),
                   category.getReferenceUnit(),
                   flow.getName(),
                   flow.getCategory().getCategory().getName(),
                   flow.getCategory().getName(),
                   factor.getUnit().getName(),
                   flow.getRefId(),
                   factor.getValue()]
            rows.append(row)

    with codecs.open(EXPORT_PATH, 'w', 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['LCIA-Method', 'LCIA-Category', 'Ref.Unit',
                         'Flow', 'Compartment', 'Sub-Compartment',
                         'Unit', 'Flow-UUID', 'Amount'])
        for r in rows:
            writer.writerow(r)

if __name__ == '__main__':
    main()
