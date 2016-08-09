import iomb.model as model
import iomb.refmap as ref
import iomb.sat as sat
import iomb.ia as ia
import pandas as pd


class ValidationResult(object):
    def __init__(self):
        self.display_message_count = 10
        self.failed = False
        self.errors = []
        self.warnings = []
        self.information = []

    def fail(self, message):
        self.errors.insert(0, 'invalid model: ' + message)
        self.failed = True
        return self


def validate(m: model.Model) -> ValidationResult:
    vr = ValidationResult()
    if not isinstance(m, model.Model):
        return vr.fail('not an instance of iomb.model.Model')
    _check_field_types(m, vr)

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


class Message(object):
    def __init__(self, message, message_type):
        self.message = message
        self.message_type = message_type

    def __str__(self):
        return '%s - %s' % (self.message_type, self.message)

    def _repr_html_(self):
        """
        HTML representation of a validation method for the display in Jupyter
        workbooks.
        """
        color = '#2E4172'
        if self.message_type == Message.ERROR:
            color = '#AA3939'
        if self.message_type == Message.WARNING:
            color = '#C7C732'
        return '<p style="color:%s;">%s - %s</h1>' % (color, self.message_type,
                                                      self.message)


class Validation(object):
    def __init__(self, title='Validation'):
        self.title = title
        self.messages = []

    def error(self, message=''):
        m = Message(message, Message.ERROR)
        self.messages.append(m)

    def warn(self, message=''):
        m = Message(message, Message.WARNING)
        self.messages.append(m)

    def info(self, message=''):
        m = Message(message, Message.INFO)
        self.messages.append(m)

    def _repr_html_(self):
        html = '<h3>%s</h3>' % self.title
        errors, warnings, infos = 0, 0, 0
        for m in self.messages:
            if m.message_type == Message.ERROR:
                errors += 1
            elif m.message_type == Message.WARNING:
                warnings += 1
            else:
                infos += 1
        stats = (errors, warnings, infos)
        html += '<p>%s errors, %s warnings, %s information: </p>' % stats

        def key_fn(msg: Message) -> int:
            if msg.message_type == Message.ERROR:
                return 0
            if msg.message_type == Message.WARNING:
                return 1
            return 3

        self.messages.sort(key=key_fn)
        for m in self.messages:
            html += m._repr_html_()
        return html
