import iomb.util as util


class ElemFlow(object):
    """ Describes an elementary flow in the satellite table. """

    def __init__(self, name='', category='', sub_category='', unit='kg',
                 uid=None):
        self.name = name
        self.category = category
        self.sub_category = sub_category
        self.unit = unit
        if uid is not None:
            self.uid = uid
        else:
            self.uid = util.uuid_of_flow(name, category, sub_category, unit)
        self.direction = 'output'
        self.factor = 1
        self.property_uid = ''
        self.unit_uid = ''

    @property
    def key(self):
        return util.as_path(self.category, self.sub_category, self.name,
                            self.unit)


class Sector(object):
    def __init__(self, name='', code='', location='US'):
        self.name = name
        self.code = code
        self.location = location
        self.uid = util.uuid_of_process(name, code, location)
        self.product_uid = util.uuid_of_product(name, code, location)
        self.category = ''
        self.sub_category = ''

    @property
    def key(self):
        return util.as_path(self.code, self.name, self.location)
