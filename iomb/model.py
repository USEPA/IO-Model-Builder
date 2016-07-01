import pandas as pd
import iomb.sat as sat
import iomb.refmap as ref
import logging as log


class Model(object):
    """ Bundles all information of an EE-IO model. Not all tasks that can be
        done with iomb require all that information. Thus, it is possible to
        create instances of this class where only the required fields are
        initialized and use them in the specific tasks. """

    def __init__(self, drc_matrix: pd.DataFrame, sat_table: sat.Table,
                 sectors: ref.SectorMap, units: ref.UnitMap,
                 compartments: ref.CompartmentMap, locations: ref.LocationMap):
        self.drc_matrix = drc_matrix
        self.sat_table = sat_table
        self.sectors = sectors
        self.units = units
        self.compartments = compartments
        self.locations = locations

    def sectors(self):
        for sector_key in self.drc_matrix.columns:
            sector = self.sectors.get(sector_key)
            if sector is None:
                log.warning('No metadata for sector: %s', sector_key)
            else:
                yield sector
