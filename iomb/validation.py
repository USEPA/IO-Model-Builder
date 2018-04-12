import iomb.model as model
import iomb.refmap as ref
import iomb.sat as sat
import iomb.ia as ia
import pandas as pd
import logging as log


class ValidationResult(object):
    def __init__(self):
        self.display_count = 5
        self.failed = False
        self.errors = []
        self.warnings = []
        self.information = []

    def fail(self, message):
        self.errors.insert(0, 'invalid model: ' + message)
        self.failed = True
        return self

    def __str__(self):
        t = 'Validation result:\n\n'
        c_errors, c_warnings = len(self.errors), len(self.warnings)
        if c_errors == 0 and c_warnings == 0:
            t += ' no errors or warnings, everything seems to be fine\n\n'
        else:
            t += ' there are %s errors and %s warnings\n\n' % (c_errors,
                                                               c_warnings)
        t += self._list_str('errors', self.errors)
        t += self._list_str('warnings', self.warnings)
        t += self._list_str('information', self.information)
        return t

    def _repr_html_(self):
        """ HTML representation of a validation result for the display in
            Jupyter workbooks. """
        t = '<div><h1>Validation result</h1>'
        c_errors, c_warnings = len(self.errors), len(self.warnings)
        if c_errors == 0 and c_warnings == 0:
            t += '<p style="color:#2E4172">no errors or warnings, everything ' \
                 'seems to be fine</p>'
        else:
            t += '<p style="color:#AA3939">there are %s errors and %s warnings' \
                 '</p>' % (c_errors, c_warnings)
        t += self._list_html('errors', self.errors, '#AA3939')
        t += self._list_html('warnings', self.warnings, '#C7C732')
        t += self._list_html('information', self.information, '#2E4172')
        t += '</div>'
        return t

    def _list_str(self, title: str, messages: list) -> str:
        if len(messages) == 0:
            return ''
        t = " %s:\n" % title
        for i in range(0, len(messages)):
            if self.display_count >= 0 and i >= self.display_count:
                r = len(messages) - self.display_count
                t += '  * %s more\n' % r
                break
            t += '  * %s\n' % messages[i]
        t += '\n'
        return t

    def _list_html(self, title: str, messages: list, color: str) -> str:
        if len(messages) == 0:
            return ''
        t = '<h3 style="color:%s">%s</h3><ul>' % (color, title)
        for i in range(0, len(messages)):
            if self.display_count >= 0 and i >= self.display_count:
                r = len(messages) - self.display_count
                t += '<li style="color:%s">%s more</li>' % (color, r)
                break
            t += '<li style="color:%s">%s</li>' % (color, messages[i])
        t += '</ul>'
        return t


def validate(m: model.Model) -> ValidationResult:
    log.info('validate model')
    vr = ValidationResult()
    if not isinstance(m, model.Model):
        return vr.fail('not an instance of iomb.model.Model')
    _check_field_types(m, vr)
    _check_sat_units(m, vr)
    _check_sat_compartments(m, vr)
    _check_sat_sectors(m, vr)
    _check_sector_locations(m, vr)
    _check_flow_uids(m, vr)
    _check_ia_coverage(m, vr)
    _check_duplicate_flow_uids(m, vr)
    return vr


def _check_field_types(m: model.Model, vr: ValidationResult):
    # field checks: (field value, type, field name, optional)
    field_checks = [
        (m.drc_matrix, pd.DataFrame, 'drc_matrix', False),
        (m.sat_table, sat.Table, 'sat_table', False),
        (m.sectors, ref.SectorMap, 'sectors', False),
        (m.ia_table, ia.Table, 'ia_table', True),
        (m.units, ref.UnitMap, 'units', True),
        (m.compartments, ref.CompartmentMap, 'compartments', True),
        (m.locations, ref.LocationMap, 'locations', True)
    ]
    for field in field_checks:
        value = field[0]
        optional = field[3]
        if optional and value is None:
            continue
        if not isinstance(value, field[1]):
            vr.fail('field %s is not an instance of %s' % (field[2], field[1]))
            break
    if m.ia_table is None:
        vr.information.append('model without LCIA data')


def _check_sector_locations(m: model.Model, vr: ValidationResult):
    unknown_codes = []
    for key in m.sectors.mappings.keys():
        sector = m.sectors.get(key)
        code = sector.location
        if code in unknown_codes:
            continue
        location = m.locations.get(code)
        if location is None:
            vr.warnings.append('unknown location %s' % code)
            unknown_codes.append(code)
    if len(unknown_codes) == 0:
        vr.information.append('all location codes of sectors are ok')


def _check_ia_coverage(m: model.Model, vr: ValidationResult):
    if m.ia_table is None:
        return
    uncovered_count = 0
    for flow in m.sat_table.flows:
        covered = False
        for category in m.ia_table.categories:
            factor = m.ia_table.get_factor(category, flow)
            if factor != 0:
                covered = True
                break
        if not covered:
            uncovered_count += 1
            vr.warnings.append('flow %s is not covered by the LCIA model' %
                               flow)
    if uncovered_count == 0:
        vr.information.append('all flows covered by LCIA model')


def _check_sat_units(m: model.Model, vr: ValidationResult):
    unknown_units = []
    for flow in m.sat_table.flows:
        unit_name = flow.unit
        if unit_name in unknown_units:
            continue
        unit = m.units.get(unit_name)
        if unit is None:
            unknown_units.append(unit_name)
            vr.errors.append('Unit %s of flow %s is unknown' % (unit_name,
                                                                flow))
    if len(unknown_units) == 0:
        vr.information.append('all units in satellite table are known')


def _check_sat_compartments(m: model.Model, vr: ValidationResult):
    unknown = []
    for flow in m.sat_table.flows:
        ck = flow.compartment_key
        if ck in unknown:
            continue
        if ck != "/":
            c = m.compartments.get(ck)
        if c is None:
            unknown.append(ck)
            vr.errors.append('Compartment %s of flow %s is unknown' % (ck,
                                                                       flow))
    if len(unknown) == 0:
        vr.information.append('all compartments in satellite table are known')


def _check_sat_sectors(m: model.Model, vr: ValidationResult):
    """ Check that the sectors from the satellite tables match the sectors in
        the direct requirements matrix. """
    unknown = []
    for sector in m.sat_table.sectors:
        key = sector.key
        if key in unknown:
            continue
        if key not in m.drc_matrix.index:
            unknown.append(key)
            vr.errors.append('Sector %s in satellite matrix does not match a'
                             ' sector in the direct requirements matrix' % key)
    if len(unknown) == 0:
        vr.information.append('all sectors in the satellite matrix match a'
                              ' sector in the direct requirements matrix')


def _check_flow_uids(m: model.Model, vr: ValidationResult):
    """ Checks if flows with the same key attributes (name, category, unit,
        etc.) have also the same UUIDs in the satellite and LCIA table. """
    if m.sat_table is None or m.ia_table is None:
        return
    errors = False
    for sat_flow in m.sat_table.flows:
        ia_flow = m.ia_table.get_flow(sat_flow.key)
        if ia_flow is None or sat_flow.uid == ia_flow.uid:
            continue
        errors = True
        vr.errors.append('Flow %s has different UUIDs in the satellite and LCIA'
                         ' table (%s <> %s)' % (sat_flow.key, sat_flow.uid,
                                                ia_flow.uid))
    if not errors:
        vr.information.append('all elementary flows have the same UUIDs in the'
                              ' satellite and LCIA table')


def _check_duplicate_flow_uids(m: model.Model, vr: ValidationResult):
    """ Check if different flows have the same UUID in the satellite table """
    checks = {}
    errors = []
    for flow in m.sat_table.flows:
        key = checks.get(flow.uid)
        if key is None:
            checks[flow.uid] = flow.key
        elif key != flow.key:
            log_it = False
            if key not in errors:
                errors.append(key)
                log_it = True
            if flow.key not in errors:
                errors.append(flow.key)
                log_it = True
            if log_it:
                vr.errors.append('Flow %s has the same UUID = %s as flow %s' % (flow.key, flow.uid, key))
    if len(errors) == 0:
        vr.information.append('all flow UUIDs in the satellite table are unique')
