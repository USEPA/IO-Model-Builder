"""
This module contains methods for writing impact assessment methods to JSON-LD
packages.
"""
import iomb.model as mod
import iomb.util as util
import logging as log


def check_export_lcia_method(model: mod.Model, pack, dump_fn):
    ia_table = model.ia_table
    if ia_table is None:
        return
    _write_method(dump_fn, ia_table, pack)
    for category in ia_table.categories:
        log.info('Write LCIA category %s', category.name)
        c = {
            "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
            "@type": "ImpactCategory",
            "@id": category.uid,
            "name": category.name,
            "referenceUnitName": category.ref_unit,
            "impactFactors": []}
        for flow in ia_table.flows:
            val = ia_table.get_factor(category, flow)
            if val == 0:
                continue
            unit = flow.get_unit(model.units)
            if unit is None:
                log.error('unknown flow unit %s', flow.key)
                continue
            f = {"@type": "ImpactFactor",
                 "value": val,
                 "flow": {"@type": "Flow", "@id": flow.uid},
                 "unit": {"@type": "Unit", "@id": unit.unit_uid},
                 "flowProperty": {
                     "@type": "FlowProperty",
                     "@id": unit.quantity_uid}}
            c['impactFactors'].append(f)
        dump_fn(c, 'lcia_categories', pack)


def _write_method(dump_fn, ia_table, pack):
    log.info('Write LCIA method %s', ia_table.method)
    m = {
        "@context": "http://greendelta.github.io/olca-schema/context.jsonld",
        "@type": "ImpactMethod",
        "@id": util.make_uuid(ia_table.method),
        "name": ia_table.method,
        "impactCategories": []}
    for category in ia_table.categories:
        c = {"@type": "ImpactCategory",
             "@id": category.uid,
             "name": category.name}
        m['impactCategories'].append(c)
    dump_fn(m, 'lcia_methods', pack)
