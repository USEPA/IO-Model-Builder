"""
This module contains functions that map entities like units, locations,
compartments, etc. to reference data with UUIDs.
"""

import logging as log

__units = None


class UnitMapping(object):
    def __init__(self, name: str, unit_uid: str, property_name: str,
                 property_uid: str, factor: float):
        self.name = name
        self.unit_uid = unit_uid
        self.property_name = property_name
        self.property_uid = property_uid
        self.factor = factor


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


def map_unit(unit_name: str) -> UnitMapping:
    if __units is None:
        __init_units()
    unit = unit_name.strip().lower()
    if unit in __units:
        return __units[unit]
    else:
        log.error('Could not map unknown unit: %s' % unit)
        return UnitMapping(unit_name, '', '', '', 1.0)
