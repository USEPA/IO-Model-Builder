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
        """ The key identifies an elementary flow in the model builder (e.g. in
            indices of data frames, results etc.). It is just a combination of
            the following flow attributes with all letters in lower case:

            <category>/<sub_category>/<name>/<unit>

            e.g.: air/unspecified/carbon dioxide/kg
        """
        return util.as_path(self.category, self.sub_category, self.name,
                            self.unit)


class Sector(object):
    """ Describes an industry or commodity sector in the input-output model. """

    def __init__(self, name='', code='', location='US', unit='USD'):
        self.name = name
        self.code = code
        self.location = location
        self.unit = unit
        self.category = ''
        self.sub_category = ''

    @property
    def key(self):
        """ The key identifies sector in the model builder (e.g. in indices of
            make and use tables, results etc.). It is just a combination of
            the following sector attributes with all letters in lower case:

            <sector code>/<sector name>/<location code>

            e.g.: 1111a0/oilseed farming/us
        """
        return util.as_path(self.code, self.name, self.location)

    @property
    def uid(self):
        return util.make_uuid('Process', self.key)

    @property
    def product_uid(self):
        return util.make_uuid('Flow', self.key)
