import os.path as path
import pandas as pd
import iomb.calc as calc
import iomb.io as io
import iomb.sat as sat
import logging as log
import sys

log.basicConfig(level=log.WARNING, format='%(levelname)s %(message)s',
                stream=sys.stdout)


def log_all():
    """ By default we only log warnings. This function sets the log-level to
        DEBUG so that all logs of the iomb package are written to the standard
        output.
    """
    log.getLogger().setLevel(level=log.DEBUG)


def make_io_model(supply_table_csv, use_table_csv, scrap_sectors=None) \
        -> io.Model:
    """ Constructs the input-output model from the supply and use tables in the
        given CSV files.
    """
    log.info('Create IO model')
    supply_table = read_csv_data_frame(supply_table_csv)
    use_table = read_csv_data_frame(use_table_csv)
    return io.Model(use_table, supply_table, scrap_sectors)


def make_sat_table(*args: list) -> sat.Table:
    """ Constructs the satellite table from the given CSV files. """
    log.info('Create satellite table')
    table = sat.Table()
    for csv_file in args:
        table.add_file(csv_file)
    return table


def calculate(io_model: io.Model, sat_table: sat.Table, demand: dict) \
        -> calc.Result:
    """ Calculates the given input-output model with the given demand. """
    drc_frame = io_model.get_dr_coefficients()
    sat_frame = sat_table.as_data_frame()
    return calc.Calculator(drc_frame, sat_frame, demand).calculate()


def read_csv_data_frame(csv_file) -> pd.DataFrame:
    """ Loads a pandas DataFrame from the given CSV file. """
    log.info('read data frame from %s', csv_file)
    df = pd.read_csv(csv_file, index_col=0, header=0)
    df.fillna(0.0, inplace=True)

    def strip(x): return x.strip()

    df.rename(index=strip, columns=strip, inplace=True)
    return df
