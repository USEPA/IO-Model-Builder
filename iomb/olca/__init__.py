import json
import iomb.util as util
import iomb.model as mod
import iomb.refmap as ref
from .dqx import append_data_quality, dq_process_system, dq_exchanges_system
from .iax import export_lcia_method
import logging as log
import zipfile as zipf


class Export(object):
    """ Exports data into a JSON-LD package for openLCA. """

    def __init__(self, model: mod.Model, with_data_quality=False, cutoff=0.0):
        self.model = model
        self.with_data_quality = with_data_quality
        self.cutoff = cutoff

    def to(self, zip_file):
        pack = zipf.ZipFile(zip_file, mode='a', compression=zipf.ZIP_DEFLATED)
        _write_economic_units(pack)
        _write_compartments(self.model.compartments, pack)
        _write_satellite_flows(self.model, pack)
        _write_locations(self.model, pack)
        if self.with_data_quality:
            dump(dq_process_system(), 'dq_systems', pack)
            dump(dq_exchanges_system(), 'dq_systems', pack)

        self.__write_sector_categories(pack)
        self.__write_products(pack)
        for s in self.model.each_sector():
            log.info('Create process %s', s.key)
            p = self.__prepare_process(s)
            self.__add_tech_inputs(s, p)
            self.__add_elem_entries(s, p)
            dump(p, 'processes', pack)
        export_lcia_method(self.model, pack, dump)
        pack.close()

    def __write_sector_categories(self, pack):
        handled = []
        for s in self.model.each_sector():
            cat = s.category
            if cat not in handled:
                handled.append(cat)
                _write_category('PROCESS', cat, pack)
                _write_category('FLOW', cat, pack)
            sub = s.sub_category
            sub_path = util.as_path(cat, sub)
            if sub_path not in handled:
                handled.append(sub_path)
                _write_category('PROCESS', sub, pack, parent_name=cat)
                _write_category('FLOW', sub, pack, parent_name=cat)

    def __write_products(self, pack):
        for s in self.model.each_sector():
            cat_id = util.make_uuid('FLOW', s.sub_category, s.category)
            flow = {
                "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
                "@type": "Flow",
                "@id": s.product_uid,
                "name": s.name,
                "category": {"@type": "Category", "@id": cat_id},
                "flowType": "PRODUCT_FLOW",
                "flowProperties": [{
                    "@type": "FlowPropertyFactor",
                    "referenceFlowProperty": True,
                    "conversionFactor": 1.0,
                    "flowProperty": {
                        "@type": "FlowProperty",
                        "@id": "b0682037-e878-4be4-a63a-a7a81053a691"
                    }}]}
            loc = self.model.locations.get(s.location)
            if loc is not None:
                flow["location"] = {"@type": "Location", "@id": loc.uid}
            dump(flow, 'flows', pack)

    def __add_tech_inputs(self, s: ref.Sector, p: dict):
        exchanges = p["exchanges"]
        col_key = s.key
        for row_s in self.model.each_sector():
            row_key = row_s.key
            val = self.model.drc_matrix.at[row_key, col_key]
            if abs(val) <= self.cutoff:
                continue
            e = {
                "@type": "Exchange",
                "avoidedProduct": False,
                "input": True,
                "amount": val,
                "flow": {"@type": "Flow", "@id": row_s.product_uid},
                "unit": {
                    "@type": "Unit",
                    "@id": "3f90ee51-c78b-4b15-a693-e7f320c1e894"
                },
                "flowProperty": {
                    "@type": "FlowProperty",
                    "@id": "b0682037-e878-4be4-a63a-a7a81053a691"
                },
                "quantitativeReference": False
            }
            if self.with_data_quality:
                # TODO: currently a default value
                e['dqEntry'] = '(1;3;1;1;1)'
            exchanges.append(e)

    def __add_elem_entries(self, s: ref.Sector, p: dict):
        sat = self.model.sat_table
        if s.key not in sat.sector_idx:
            # log.warning('%s is not contained in satellite matrix', s.key)
            return
        exchanges = p["exchanges"]
        for flow in sat.flows:
            entry = sat.get_entry(flow.key, s.key)
            if entry is None or entry.value == 0:
                continue
            compartment = flow.get_compartment(self.model.compartments)
            unit = flow.get_unit(self.model.units)
            if compartment is None or unit is None:
                continue
            is_input = compartment.direction == 'input'
            e = {
                "@type": "Exchange",
                "avoidedProduct": False,
                "input": is_input,
                "amount": entry.value,
                "flow": {"@type": "Flow", "@id": flow.uid},
                "unit": {"@type": "Unit",
                         "@id": unit.unit_uid},
                "flowProperty": {"@type": "FlowProperty",
                                 "@id": unit.quantity_uid},
                "quantitativeReference": False,
                "comment":  Export.__sat_entry_comment(entry)
            }
            if self.with_data_quality and entry.data_quality_entry is not None:
                e['dqEntry'] = entry.data_quality_entry
            exchanges.append(e)

    @staticmethod
    def __sat_entry_comment(e) -> str:
        """ :type e: iomb.sat.Entry """
        if e is None:
            return None

        def append(cmt: str, label: str, field: str) -> str:
            if field is None:
                return cmt
            if cmt is None:
                return "%s: %s" % (label, field)
            return "%s; %s: %s" % (cmt, label, field)

        comment = append(None, 'Year', e.year)
        comment = append(comment, 'Tags', e.tags)
        comment = append(comment, 'Soures', e.sources)
        return append(comment, 'Other', e.comment)

    def __prepare_process(self, s: ref.Sector):
        cat_id = util.make_uuid('PROCESS', s.sub_category, s.category)
        p = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": "Process",
            "@id": s.uid,
            "name": s.name,
            "processTyp": "UNIT_PROCESS",
            "category": {"@type": "Category", "@id": cat_id},
            "processDocumentation": {"copyright": False},
            "exchanges": [{
                "@type": "Exchange",
                "avoidedProduct": False,
                "input": False,
                "amount": 1.0,
                "flow": {"@type": "Flow", "@id": s.product_uid},
                "unit": {"@type": "Unit",
                         "@id": "3f90ee51-c78b-4b15-a693-e7f320c1e894"},
                "flowProperty": {"@type": "FlowProperty",
                                 "@id": "b0682037-e878-4be4-a63a-a7a81053a691"},
                "quantitativeReference": True}]
        }
        Export.__add_doc_fields(p, s)
        loc = self.model.locations.get(s.location)
        if loc is not None:
            p["location"] = {"@type": "Location", "@id": loc.uid}
        if self.with_data_quality:
            append_data_quality(p, s)
        return p

    @staticmethod
    def __add_doc_fields(p: dict, s: ref.Sector):
        if s.csv_row is None:
            return
        if len(s.csv_row) < 6:
            return
        p["description"] = s.csv_row[5]
        fn = Export.__add_doc_field
        fn(s.csv_row, 6, p, "validFrom")
        fn(s.csv_row, 7, p, "validUntil")
        fn(s.csv_row, 8, p, "geographyDescription")
        fn(s.csv_row, 9, p, "technologyDescription")
        fn(s.csv_row, 10, p, "intendedApplication")
        # TODO 11..13 data set owner, generator, and documentor
        fn(s.csv_row, 14, p, "restrictionsDescription")
        fn(s.csv_row, 15, p, "projectDescription")
        fn(s.csv_row, 16, p, "inventoryMethodDescription")
        fn(s.csv_row, 17, p, "modelingConstantsDescription")
        fn(s.csv_row, 18, p, "completenessDescription")
        fn(s.csv_row, 19, p, "dataTreatmentDescription")
        fn(s.csv_row, 20, p, "samplingDescription")
        fn(s.csv_row, 21, p, "dataCollectionDescription")
        # TODO 22 reviewer
        fn(s.csv_row, 23, p, "reviewDetails")
        # TODO 26.. sources

    @staticmethod
    def __add_doc_field(csv_row: list, idx: int, p: dict, field: str):
        if idx >= len(csv_row):
            return
        val = csv_row[idx]
        if val is None:
            return
        if not isinstance(val, str):
            val = str(val)
        val = val.strip()
        if val == '':
            return
        p["processDocumentation"][field] = val


def _write_category(model_type, name, pack, parent_name=None):
    uid = util.make_uuid(model_type, name, parent_name)
    c = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "Category",
        "@id": uid,
        "name": name,
        "modelType": model_type
    }
    if parent_name is not None:
        parent_id = util.make_uuid(model_type, parent_name)
        # to be compatible with openLCA 1.4 and 1.5 we use 'category' and
        # 'parentCategory'
        c["category"] = {"@type": "Category", "@id": parent_id}
        c["parentCategory"] = {"@type": "Category", "@id": parent_id}
    dump(c, 'categories', pack)


def _write_satellite_flows(model: mod.Model, pack: zipf.ZipFile):
    for flow in model.sat_table.flows:
        unit = flow.get_unit(model.units)
        if unit is None:
            log.error('unknown unit %s in flow %s', flow.unit, flow.key)
            continue
        f = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": "Flow",
            "@id": flow.uid,
            "name": flow.name,
            "cas": flow.cas_number,
            "flowType": "ELEMENTARY_FLOW",
            "flowProperties": [{
                "@type": "FlowPropertyFactor",
                "referenceFlowProperty": True,
                "conversionFactor": 1.0,
                "flowProperty": {
                    "@type": "FlowProperty",
                    "name": unit.quantity,
                    "@id": unit.quantity_uid
                }}]}
        compartment = flow.get_compartment(model.compartments)
        if compartment is not None:
            f["category"] = {"@type": "Category", "@id": compartment.uid}
        dump(f, 'flows', pack)


def _write_locations(model: mod.Model, pack: zipf.ZipFile):
    used_codes = []
    for sector in model.each_sector():
        if sector.location not in used_codes:
            used_codes.append(sector.location)
    for code in used_codes:
        loc = model.locations.get(code)
        if loc is None:
            log.error('unknown location %s', code)
            continue
        l = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": "Location",
            "@id": loc.uid,
            "name": loc.name,
            "code": loc.code
        }
        dump(l, 'locations', pack)


def _write_economic_units(pack):
    ug = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "UnitGroup",
        "@id": "5df2915b-186f-4773-9ef4-04baca5e56a9",
        "name": "Units of currency 2007",
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
        "name": "Market value US 2007",
        "flowPropertyType": "ECONOMIC_QUANTITY",
        "unitGroup": {
            "@type": "UnitGroup",
            "@id": "5df2915b-186f-4773-9ef4-04baca5e56a9"
        }}
    dump(fp, 'flow_properties', pack)


def _write_compartments(comp_map: ref.CompartmentMap, pack: zipf.ZipFile):
    if comp_map is None:
        return

    def get_parent_uid(name):
        for pc in comp_map.mappings.values():
            if pc.compartment != name:
                continue
            if pc.sub_compartment is None or pc.sub_compartment == '':
                return pc.uid
        return None

    written = []
    for comp in comp_map.mappings.values():
        if comp.uid in written:
            continue
        written.append(comp.uid)
        c = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": "Category",
            "modelType": "FLOW",
            "@id": comp.uid}
        if comp.sub_compartment is None or comp.sub_compartment == '':
            c["name"] = comp.compartment
        else:
            c["name"] = comp.sub_compartment
            parent_uid = get_parent_uid(comp.compartment)
            if parent_uid is not None:
                c["category"] = {"@type": "Category", "@id": parent_uid}
        dump(c, 'categories', pack)


def dump(obj: dict, folder: str, pack: zipf.ZipFile):
    """ dump writes the given dictionary to the zip-file under the given folder.
    """
    uid = obj.get('@id')
    if uid is None or uid == '':
        log.error('No @id for object %s in %s', obj, folder)
        return
    path = '%s/%s.json' % (folder, obj['@id'])
    s = json.dumps(obj)
    pack.writestr(path, s)
