"""
This module contains types and functions that map entities like units, locations,
compartments, flows etc. to reference data with UUIDs.
"""
from .data import data_dir
from .util import each_csv_row, as_path, make_uuid


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


class ElemFlow(object):
    """ Describes an elementary flow in the satellite table. """

    def __init__(self):
        self.name = ''
        self.category = ''
        self.sub_category = ''
        self.unit = ''
        self.uid = ''
        self.cas_number = ''

    @staticmethod
    def from_satellite_row(csv_row):
        """ Creates an flow instance from the information in a CSV row of a
            satellite table. """
        f = ElemFlow()
        f.name = csv_row[0]
        f.cas_number = csv_row[1]
        f.category = csv_row[2]
        f.sub_category = csv_row[3]
        f.uid = csv_row[4]
        f.unit = csv_row[9]
        return f

    @property
    def key(self):
        """ The key identifies an elementary flow in the model builder (e.g. in
            indices of data frames, results etc.). It is just a combination of
            the following flow attributes with all letters in lower case:

            <category>/<sub_category>/<name>/<unit>

            e.g.: air/unspecified/carbon dioxide/kg
        """
        return as_path(self.category, self.sub_category, self.name, self.unit)

    @property
    def compartment_key(self):
        return as_path(self.category, self.sub_category)


class Sector(object):
    """ Describes an industry or commodity sector in the input-output model. """

    def __init__(self, name='', code='', location='US', unit='USD'):
        self.name = name
        self.code = code
        self.location = location
        self.unit = unit
        self.category = ''
        self.sub_category = ''
        self.location_uid = ''

    @property
    def key(self):
        """ The key identifies sector in the model builder (e.g. in indices of
            make and use tables, results etc.). It is just a combination of
            the following sector attributes with all letters in lower case:

            <sector code>/<sector name>/<location code>

            e.g.: 1111a0/oilseed farming/us
        """
        return as_path(self.code, self.name, self.location)

    @property
    def uid(self):
        return make_uuid('Process', self.key)

    @property
    def product_uid(self):
        return make_uuid('Flow', self.key)
