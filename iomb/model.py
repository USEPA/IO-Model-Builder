import pandas as pd
import iomb.sat as sat

class Model(object):
    def __init__(self, drc_matrix: pd.DataFrame, sat_table: sat.Table,
                 sector_info_csv='', unit_info_csv='', compartment_info_csv='',
                 location_info_csv=''):
        drc_matrix = None  # the direct requirements coefficients matrix
