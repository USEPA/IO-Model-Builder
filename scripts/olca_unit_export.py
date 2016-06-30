"""
This script exports the default physical units from openLCA to a file that can
be directly used as unit mapping file in the iomb package. When preparing the
file for iomb also have a look on possible logging warnings for duplicates.

Note that this script should be executed within openLCA.
"""

import codecs
import csv
import org.openlca.core.model.FlowPropertyType as FT

# set this path to the file where the locations should be written
EXPORT_PATH = 'C:/Users/Besitzer/Desktop/unit_meta_data.csv'


def main():
    global olca, log
    entries = []
    fn = make_collector(entries)
    olca.eachUnitGroup(fn)
    entries.sort(key=lambda x: x[0].lower())
    check_entries(entries)
    with codecs.open(EXPORT_PATH, 'w', 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Unit', 'Unit-UUID', 'Quantity', 'Quantity-UUID'])
        for e in entries:
            writer.writerow(e)


def make_collector(entries):
    """ Creates a function that collects unit mappings and adds them to the
        given list. """
    global log

    def fn(unit_group):
        prop = unit_group.getDefaultFlowProperty()
        if prop is None or prop.getFlowPropertyType() != FT.PHYSICAL:
            return
        log.info('export unit group {}', unit_group)
        for unit in unit_group.getUnits():
            entry = [unit.getName(), unit.getRefId(), prop.getName(),
                     prop.getRefId()]
            entry = [e.strip() for e in entry]
            entries.append(entry)
            # also add unit synonyms
            syns = unit.getSynonyms()
            if syns is not None and syns != '':
                for syn in syns.strip().split(';'):
                    syn_entry = [syn.strip(), entry[1], entry[2], entry[3]]
                    entries.append(syn_entry)

    return fn


def check_entries(entries):
    global log
    m = {}
    for e in entries:
        unit_name = e[0]
        unit_uuid = e[1]
        if unit_name in m:
            dup_id = m[unit_name]
            if dup_id != unit_uuid:
                log.warn('duplicate entry for unit {} with different IDs!',
                         unit_name)
        else:
            m[unit_name] = unit_uuid


if __name__ == '__main__':
    main()
