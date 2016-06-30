"""
This module contains functions that map entities like units, locations,
compartments, etc. to reference data with UUIDs.
"""
from .data import data_dir
from .util import each_csv_row
import logging as log


class UnitEntry(object):
    """ Describes an entry in a unit-mapping file. In iomb units are mapped by
        name. """

    def __init__(self):
        self.unit_name = ''
        self.unit_uid = ''
        self.quantity_name = ''
        self.quantity_uid = ''

    @staticmethod
    def from_csv(csv_row):
        e = UnitEntry()
        e.unit_name = csv_row[0]
        e.unit_uid = csv_row[1]
        e.quantity_name = csv_row[2]
        e.quantity_uid = csv_row[3]
        return e


class UnitMap(object):
    def __init__(self):
        self.mappings = {}

    @staticmethod
    def read(file_path):
        m = UnitMap()

        def row_handler(row, i):
            e = UnitEntry.from_csv(row)
            m.mappings[e.unit_name] = e

        each_csv_row(file_path, row_handler, skip_header=True)
        return m

    @staticmethod
    def create_default():
        """ Creates the unit map with default data. """
        path = data_dir + '/unit_meta_data.csv'
        return UnitMap.read(path)

    def get(self, unit_name: str) -> UnitEntry:
        if unit_name in self.mappings:
            return self.mappings[unit_name]
        return None


class LocationMapping(object):
    def __init__(self, code, name, uid):
        self.code = code
        self.name = name
        self.uid = uid


def __init_locations():
    global __locations
    __locations = {
        'us': LocationMapping('US', 'United States',
                              '0b3b97fa-6688-3c56-88ee-4ae80ec0c3c2'),
        'us-ga': LocationMapping('US-GA', 'United States, Georgia',
                                 '2b701fc6-ef0e-3b9a-9f4d-631863e904f6')
    }


def map_location(location_code: str) -> LocationMapping:
    if __locations is None:
        __init_locations()
    code = location_code.strip().lower()
    if code in __locations:
        return __locations[code]
    else:
        log.error('Could not map unknown location: %s' % code)
        return LocationMapping(location_code, '', '')
