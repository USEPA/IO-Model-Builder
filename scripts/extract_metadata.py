"""
This is a script for preparing metadata files from a satellite table.
"""

import csv
import iomb.refmap as refmap


def prepare_flow_meta_data(sat, to_file: str):
    """ Prepares a flow meta data file for the conversion to openLCA with
        the elementary flow information from this table and writes it to
        the given location
    """
    with open(to_file, 'w', encoding='utf-8', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Category', 'Subcategory', 'Unit',
                         'Direction', 'Flow-UUID', 'Property-UUID',
                         'Unit-UUID', 'Factor'])
        units = refmap.UnitMap.create_default()
        for flow in sat.flows:
            unit = units.get(flow.unit)
            row = [flow.name, flow.category, flow.sub_category, flow.unit,
                   '<input | output>', flow.uid, unit.quantity_uid,
                   unit.unit_uid]
            writer.writerow(row)


def prepare_sector_meta_data(sat, to_file: str):
    """ Prepares a sector meta data file for the conversion to openLCA with
        the sector/process information from this table. The file is written
        to the given location.
    """
    with open(to_file, 'w', encoding='utf-8', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(['Code', 'Name', 'Category', 'Sub-category',
                         'Location-Code', 'Location-UUID'])
        locations = refmap.LocationMap.create_default()
        for sector in sat.sectors:
            lm = locations.get(sector.location)
            row = [sector.code, sector.name, sector.category,
                   sector.sub_category, lm.code, lm.uid]
            writer.writerow(row)