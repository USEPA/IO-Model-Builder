import iomb
import json
import zipfile as zipf


class Export(object):
    """ Exports data into a JSON-LD package for openLCA. """

    def __init__(self, drc_csv='', sat_csv='', sector_meta_csv='',
                 flow_meta_csv=''):
        """ Initializes the export with 4 CSV files:

            :param drc_csv the direct requirement coefficients
            :param sat_csv the satellite matrix
            :param sector_meta_csv meta data of the sectors
            :param flow_meta_csv meta data of the elementary flows
        """
        self.drc = iomb.read_csv_data_frame(drc_csv)
        self.sat = iomb.read_csv_data_frame(sat_csv)

    def to(self, zip_file):
        pack = zipf.ZipFile(zip_file, mode='a', compression=zipf.ZIP_DEFLATED)
        _write_economic_units(pack)
        pack.close()


def _write_economic_units(pack):
    ug = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "UnitGroup",
        "@id": "5df2915b-186f-4773-9ef4-04baca5e56a9",
        "name": "Units of currency 2002",
        "units": [{"@type": "Unit",
                   "@id": "3f90ee51-c78b-4b15-a693-e7f320c1e894",
                   "name": "USD",
                   "referenceUnit": True,
                   "conversionFactor": 1.0
                   }]}
    dump(ug, 'unit_groups', pack)
    fp = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "FlowProperty",
        "@id": "b0682037-e878-4be4-a63a-a7a81053a691",
        "name": "Market value US 2002",
        "flowPropertyType": "ECONOMIC_QUANTITY",
        "unitGroup": {
            "@type": "UnitGroup",
            "@id": "5df2915b-186f-4773-9ef4-04baca5e56a9"
        }}
    dump(fp, 'flow_properties', pack)


def dump(obj, folder, pack):
    path = '%s/%s.json' % (folder, obj['@id'])
    s = json.dumps(obj)
    pack.writestr(path, s)
