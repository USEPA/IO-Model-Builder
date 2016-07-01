import json
import iomb.util as util
import iomb.model as mod
import iomb.refmap as ref
import logging as log
import zipfile as zipf


class Export(object):
    """ Exports data into a JSON-LD package for openLCA. """

    def __init__(self, model: mod.Model):
        self.model = model

    def to(self, zip_file):
        pack = zipf.ZipFile(zip_file, mode='a', compression=zipf.ZIP_DEFLATED)
        _write_economic_units(pack)
        _write_satellite_flows(self.model, pack)
        _write_locations(self.model, pack)
        self.__write_sector_categories(pack)
        self.__write_products(pack)
        for s in self.model.sectors():
            p = self.__prepare_process(s)
            self.__add_tech_inputs(s, p)
            self.__add_elem_entries(s, p)
            dump(p, 'processes', pack)
        pack.close()

    def __write_sector_categories(self, pack):
        handled = []
        for s in self.model.sectors():
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
        for s in self.model.sectors():
            cat_id = util.make_uuid('FLOW', s.sub_category, s.category)
            flow = {
                "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
                "@type": "Flow",
                "@id": s.product_uid,
                "name": s.name,
                "category": {"@type": "Category", "@id": cat_id},
                "flowType": "PRODUCT_FLOW",
                "location": {"@type": "Location", "@id": s.location_uid},
                "flowProperties": [{
                    "@type": "FlowPropertyFactor",
                    "referenceFlowProperty": True,
                    "conversionFactor": 1.0,
                    "flowProperty": {
                        "@type": "FlowProperty",
                        "@id": "b0682037-e878-4be4-a63a-a7a81053a691"
                    }}]
            }
            dump(flow, 'flows', pack)

    def __add_tech_inputs(self, s: ref.Sector, p: dict):
        exchanges = p["exchanges"]
        col_key = s.key
        for row_s in self.model.sectors():
            row_key = row_s.key
            val = self.model.drc_matrix.get_value(row_key, col_key)
            if val == 0:
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
            exchanges.append(e)

    def __add_elem_entries(self, s: ref.Sector, p: dict):
        sat = self.model.sat_table
        if s.key not in sat.sector_idx:
            log.warning('%s is not contained in satellite matrix', s.key)
            return
        exchanges = p["exchanges"]
        for flow in sat.flows:
            entry = sat.get_entry(flow.key, s.key)
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
                "quantitativeReference": False
            }
            exchanges.append(e)

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
        loc = self.model.locations.get(s.location)
        if loc is not None:
            p["location"] = {"@type": "Location", "@id": loc.uid}
        return p


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
    for sector in model.sectors():
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


def dump(obj: dict, folder: str, pack: zipf.ZipFile):
    path = '%s/%s.json' % (folder, obj['@id'])
    s = json.dumps(obj)
    pack.writestr(path, s)
