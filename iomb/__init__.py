import logging as log
import sys

import pandas as pd

import iomb.calc as calc
import iomb.ia as ia
import iomb.io as io
import iomb.model as model
import iomb.refmap as ref
import iomb.sat as sat
from .util import read_csv_data_frame

log.basicConfig(level=log.WARNING, format='%(levelname)s %(message)s',
                stream=sys.stdout)


def log_all(level=log.DEBUG):
    """ By default we only log warnings. This function sets the log-level to
        DEBUG so that all logs of the iomb package are written to the standard
        output.
    """
    log.getLogger().setLevel(level=level)


def make_io_model(supply_table_csv, use_table_csv, scrap_sectors=None) \
        -> io.Model:
    """ Constructs the input-output model from the supply and use tables in the
        given CSV files.
    """
    log.info('Create IO model')
    supply_table = read_csv_data_frame(supply_table_csv)
    use_table = read_csv_data_frame(use_table_csv)
    scraps = scrap_sectors
    if scraps is not None:
        scraps = [s.strip().lower() for s in scraps]
    return io.Model(use_table, supply_table, scraps)


def coefficients_from_sut(supply_table_csv: str, use_table_csv: str,
                          scrap_sectors=None) -> pd.DataFrame:
    """ Calculates the direct requirements coefficients matrix A from
        the given supply and use tables. """
    io_model = make_io_model(supply_table_csv, use_table_csv, scrap_sectors)
    return io_model.get_dr_coefficients()


def make_sat_table(*args: list) -> sat.Table:
    """ Constructs the satellite table from the given CSV files. """
    log.info('Create satellite table')
    table = sat.Table()
    for csv_file in args:
        table.add_file(csv_file)
    return table


def make_model(drc_csv: str, sat_tables: list, sector_info_csv: str,
               ia_tables=None, units_csv='', compartments_csv='',
               locations_csv='') -> model.Model:
    """
    Creates a full EE-IO model with all information required for calculations,
    JSON-LD export, validation, etc.

    :param drc_csv: CSV file with the direct requirements matrix A
    :param sat_tables: a list of CSV files with satellite tables
    :param sector_info_csv: CSV file with sector metadata
    :param ia_tables: an optional list of CSV files with impact assessment factors.
    :param units_csv: optional file with unit metadata
    :param compartments_csv: optional file with compartment metadata
    :param locations_csv: optional file with location metadata
    """
    drc = read_csv_data_frame(drc_csv)
    sat_table = make_sat_table(*sat_tables)
    sectors = ref.SectorMap.read(sector_info_csv)

    ia_table = None
    if ia_tables is not None and len(ia_tables) > 0:
        ia_table = ia.Table()
        for iat in ia_tables:
            ia_table.add_file(iat)

    def read_map(name, clazz):
        if name is None or name == '':
            return clazz.create_default()
        else:
            return clazz.read(name)

    units = read_map(units_csv, ref.UnitMap)
    compartments = read_map(compartments_csv, ref.CompartmentMap)
    locations = read_map(locations_csv, ref.LocationMap)
    return model.Model(drc, sat_table, sectors, ia_table, units, compartments,
                       locations)


def calculate(full_model: model.Model, demand: dict,
              perspective=calc.DIRECT_PERSPECTIVE) -> calc.Result:
    """
    Calculates a result for the given model and demand.

    :param full_model: The input-output model that should be calculated.
    :param demand: A dictionary containing the demand values of input-output
           sectors
    :param perspective: The perspective of the contribution results. See the
           documentation for more information about the different result
           perspectives. """
    return calc.calculate(full_model, demand, perspective)
