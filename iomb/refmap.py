"""
This module contains functions that map entities like units, locations,
compartments, etc. to reference data with UUIDs.
"""

import logging as log

__locations = None
__units = None


class UnitMapping(object):
    def __init__(self, name: str, unit_uid: str, property_name: str,
                 property_uid: str, factor: float):
        self.name = name
        self.unit_uid = unit_uid
        self.property_name = property_name
        self.property_uid = property_uid
        self.factor = factor


class LocationMapping(object):
    def __init__(self, code, name, uid):
        self.code = code
        self.name = name
        self.uid = uid


def __init_units():
    """
    Adding mappings from openLCA:

    SQL:
    select u.name as unit_name, u.ref_id as unit_uid, p.name as property_name,
    p.ref_id as property_uid from tbl_unit_groups g inner join
    tbl_flow_properties p on g.f_default_flow_property = p.id
    inner join tbl_units u on u.f_unit_group = g.id where u.name = 'kg'

    Excel:
    = "'" & LOWER(A198) & "':" & "UnitMapping('" &A198& "','" & B198 & "','"
        & C198 & "','" & D198& ", 1.0'),"

    """
    global __units
    __units = {
        'kg': UnitMapping('kg', '20aadc24-a391-41cf-b340-3e4529f44bde', 'Mass',
                          '93a60a56-a3c8-11da-a746-0800200b9a66', 1.0),
        'm2*a': UnitMapping('m2*a', 'c7266b67-4ea2-457f-b391-9b94e26e195a',
                            'Area*time',
                            '93a60a56-a3c8-21da-a746-0800200c9a66', 1.0)
    }


def __init_locations():
    global __locations
    __locations = {
        'us': LocationMapping('US', 'United States',
                              '0b3b97fa-6688-3c56-88ee-4ae80ec0c3c2'),
        'us-ga': LocationMapping('US-GA', 'United States, Georgia',
                                 '2b701fc6-ef0e-3b9a-9f4d-631863e904f6')
    }


def map_unit(unit_name: str) -> UnitMapping:
    if __units is None:
        __init_units()
    unit = unit_name.strip().lower()
    if unit in __units:
        return __units[unit]
    else:
        log.error('Could not map unknown unit: %s' % unit)
        return UnitMapping(unit_name, '', '', '', 1.0)


def map_location(location_code: str) -> LocationMapping:
    if __locations is None:
        __init_locations()
    code = location_code.strip().lower()
    if code in __locations:
        return __locations[code]
    else:
        log.error('Could not map unknown location: %s' % code)
        return LocationMapping(location_code, '', '')
