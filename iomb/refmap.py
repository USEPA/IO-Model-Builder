"""
This module contains functions that map entities like units, locations,
compartments, etc. to reference data with UUIDs.
"""
from .data import data_dir
from .util import each_csv_row, as_path


class CompartmentEntry(object):
    """ Describes an entry in a compartment-mapping file. In iomb compartments
        are mapped by the compartment and sub-compartment name. """

    def __init__(self):
        self.compartment = ''
        self.sub_compartment = ''
        self.uid = ''
        self.direction = ''

    @staticmethod
    def from_csv(csv_row):
        e = CompartmentEntry()
        e.compartment = csv_row[0]
        e.sub_compartment = csv_row[1]
        e.uid = csv_row[2]
        e.direction = csv_row[3].lower()
        return e

    @property
    def key(self):
        return as_path(self.compartment, self.sub_compartment)


class CompartmentMap(object):
    def __init__(self):
        self.mappings = {}

    @staticmethod
    def read(file_path):
        m = CompartmentMap()

        def row_handler(row, _):
            e = CompartmentEntry.from_csv(row)
            m.mappings[e.key] = e

        each_csv_row(file_path, row_handler, skip_header=True)
        return m

    @staticmethod
    def create_default():
        """ Creates the compartment map with default data. """
        path = data_dir + '/compartment_meta_data.csv'
        return CompartmentMap.read(path)

    def get(self, compartment_key: str) -> CompartmentEntry:
        key = compartment_key.strip().lower()
        if key in self.mappings:
            return self.mappings[key]
        return None


class UnitEntry(object):
    """ Describes an entry in a unit-mapping file. In iomb units are mapped by
        name. """

    def __init__(self):
        self.unit = ''
        self.unit_uid = ''
        self.quantity = ''
        self.quantity_uid = ''

    @staticmethod
    def from_csv(csv_row):
        e = UnitEntry()
        e.unit = csv_row[0]
        e.unit_uid = csv_row[1]
        e.quantity = csv_row[2]
        e.quantity_uid = csv_row[3]
        return e

    @property
    def key(self):
        return self.unit


class UnitMap(object):
    def __init__(self):
        self.mappings = {}

    @staticmethod
    def read(file_path):
        m = UnitMap()

        def row_handler(row, _):
            e = UnitEntry.from_csv(row)
            m.mappings[e.key] = e

        each_csv_row(file_path, row_handler, skip_header=True)
        return m

    @staticmethod
    def create_default():
        """ Creates the unit map with default data. """
        path = data_dir + '/unit_meta_data.csv'
        return UnitMap.read(path)

    def get(self, unit_name: str) -> UnitEntry:
        name = unit_name.strip()
        if name in self.mappings:
            return self.mappings[name]
        return None


class LocationEntry(object):
    """ Describes an entry in a location-mapping file. In iomb locations are
        mapped by location code. """

    def __init__(self):
        self.code = ''
        self.name = ''
        self.uid = ''

    @staticmethod
    def from_csv(csv_row):
        e = LocationEntry()
        e.code = csv_row[0]
        e.name = csv_row[1]
        e.uid = csv_row[2]
        return e

    @property
    def key(self):
        return self.code.lower()


class LocationMap(object):
    def __init__(self):
        self.mappings = {}

    @staticmethod
    def read(file_path):
        m = LocationMap()

        def row_handler(row, _):
            e = LocationEntry.from_csv(row)
            m.mappings[e.key] = e

        each_csv_row(file_path, row_handler, skip_header=True)
        return m

    @staticmethod
    def create_default():
        """ Creates the location map with default data. """
        path = data_dir + '/location_meta_data.csv'
        return LocationMap.read(path)

    def get(self, location_code: str) -> LocationEntry:
        key = location_code.strip().lower()
        if key in self.mappings:
            return self.mappings[key]
        return None
