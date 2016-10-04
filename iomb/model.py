import pandas as pd
import iomb.ia as ia
import iomb.refmap as ref
import iomb.sat as sat
import logging as log


class Model(object):
    """ Bundles all information of an EE-IO model. Not all tasks that can be
        done with iomb require all that information. Thus, it is possible to
        create instances of this class where only the required fields are
        initialized and use them in the specific tasks. """

    def __init__(self, drc_matrix: pd.DataFrame, sat_table: sat.Table,
                 sectors: ref.SectorMap, ia_table: ia.Table, units: ref.UnitMap,
                 compartments: ref.CompartmentMap, locations: ref.LocationMap):
        self.drc_matrix = drc_matrix
        self.sat_table = sat_table
        self.sectors = sectors
        self.ia_table = ia_table
        self.units = units
        self.compartments = compartments
        self.locations = locations

    def each_sector(self):
        for sector_key in self.drc_matrix.columns:
            sector = self.sectors.get(sector_key)
            if sector is None:
                log.warning('No metadata for sector: %s', sector_key)
            else:
                yield sector

    def sync_flow_uids(self, prefer_lcia_uids=True):
        """ Synchronizes the UUIDs of the elementary flows in the model: If
            there are flows with the same key attributes (name, category, unit
            etc.) but with different UUIDs in the satellite table and impact
            assessment model this function will align the UUIDs in both tables.
            By default it will prefer the UUIDs from the LCIA model but this
            can be changed by setting the 'prefer_lcia_uids'-parameter to False.
            """
        if self.sat_table is None or self.ia_table is None:
            log.error('Satellite table or LCIA table is None: flow'
                      'synchronization is only applicable if both tables are'
                      'in the model')
            return
        for sat_flow in self.sat_table.flows:
            ia_flow = self.ia_table.get_flow(sat_flow.key)
            if ia_flow is None or sat_flow.uid == ia_flow.uid:
                continue
            uid = None
            if prefer_lcia_uids:
                uid = ia_flow.uid
                sat_flow.uid = uid
            else:
                uid = sat_flow.uid
                ia_flow.uid = uid
            log.debug('different UUIDs for %s in sat. and LCIA table'
                      ' -> took %s', sat_flow.key, uid)