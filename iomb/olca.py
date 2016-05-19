class Export(object):
    """ Exports data into a JSON-LD package for openLCA. """

    def __init__(self, drc_csv: str, sat_csv: str, sector_meta_csv: str,
                 flow_meta_csv):
        """ Initializes the export with 4 CSV files:

            :param drc_csv the direct requirement coefficients
            :param sat_csv the satellite matrix
            :param sector_meta_csv meta data of the sectors
            :param flow_meta_csv meta data of the elementary flows
        """
        pass
