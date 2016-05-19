

class Flow(object):
    
    def __init__(self, name='', category='', sub_category='', unit=''):
        self.name = name
        self.category = category
        self.subCategory = sub_category
        self.unit = unit


class Table(object):

    def __init__(self):
        self.flows = {}