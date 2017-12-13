import csv
import json
import os

import iomb.dqi as dqi
import iomb.matio as matio
import numpy


class Sector(object):

    def __init__(self):
        self.id = ''
        self.index = 0
        self.name = ''
        self.code = ''
        self.location = ''
        self.description = ''

    def as_json_dict(self):
        return {
            'id': self.id,
            'index': self.index,
            'name': self.name,
            'code': self.code,
            'location': self.location
            'description': self.description
        }


class Indicator(object):

    def __init__(self):
        self.id = ''
        self.index = 0
        self.group = ''
        self.code = ''
        self.unit = ''
        self.name = ''

    def as_json_dict(self):
        return {
            'id': self.id,
            'index': self.index,
            'group': self.group,
            'code': self.code,
            'unit': self.unit,
            'name': self.name
        }


class Model(object):

    def __init__(self, folder: str):
        self.folder = folder  # type: str
        self.sectors = read_sectors(folder)  # type: Dict[str, Sector]
        sorted_sectors = [s for s in self.sectors.values()]
        sorted_sectors.sort(key=lambda s: s.index)
        self.sector_ids = [s.id for s in sorted_sectors]
        self.indicators = read_indicators(folder)  # type: List[Indicator]
        self.indicators.sort(key=lambda i: i.index)
        self.indicator_ids = [i.id for i in self.indicators]
        self.matrix_cache = {}

    def get_matrix(self, name: str):
        m = self.matrix_cache.get(name)
        if m is not None:
            return m
        path = '%s/%s.bin' % (self.folder, name)
        if not os.path.isfile(path):
            return None
        m = matio.read_matrix(path)
        self.matrix_cache[name] = m
        return m

    def get_dqi_matrix(self, name: str):
        m = self.matrix_cache.get(name)
        if m is not None:
            return m
        path = '%s/%s.csv' % (self.folder, name)
        if not os.path.isfile(path):
            return None
        dm = dqi.Matrix.from_csv(path)
        m = dm.to_string_list()
        self.matrix_cache[name] = m
        return m

    def calculate(self, demand):
        if demand is None:
            return
        perspective = demand.get('perspective')
        d = self.demand_vector(demand)
        data = None
        if perspective == 'direct':
            s = self.scaling_vector(d)
            D = self.get_matrix('D')
            data = scale_columns(D, s)
        elif perspective == 'intermediate':
            s = self.scaling_vector(d)
            U = self.get_matrix('U')
            data = scale_columns(U, s)
        elif perspective == 'final':
            U = self.get_matrix('U')
            data = scale_columns(U, d)
        else:
            print('ERROR: unknown perspective %s' % perspective)

        if data is None:
            print('ERROR: no data')
            return None

        result = {
            'indicators': self.indicator_ids,
            'sectors': self.sector_ids,
            'data': data.tolist()
        }
        return result

    def demand_vector(self, demand):
        L = self.get_matrix('L')
        d = numpy.zeros(L.shape[0], dtype=numpy.float64)
        entries = demand.get('demand')  # type: dict
        if entries is None:
            return d
        for e in entries:
            sector_key = e.get('sector')
            amount = e.get('amount')
            if sector_key is None or amount is None:
                continue
            amount = float(amount)
            sector = self.sectors.get(sector_key)
            if sector is None:
                continue
            d[sector.index] = amount
        return d

    def scaling_vector(self, demand_vector: numpy.ndarray) -> numpy.ndarray:
        s = numpy.zeros(demand_vector.shape[0], dtype=numpy.float64)
        L = self.get_matrix('L')
        for i in range(0, demand_vector.shape[0]):
            d = demand_vector[i]
            if d == 0:
                continue
            col = L[:, i]
            s += d * col
        return s


def read_sectors(folder: str):
    m = {}
    path = '%s/sectors.csv' % folder
    with open(path, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            s = Sector()
            s.index = int(row[0])
            s.id = row[1]
            s.name = row[2]
            s.code = row[3]
            s.location = row[4]
            s.description = row[5]
            m[s.id] = s
    return m


def read_indicators(folder: str):
    indicators = []
    path = '%s/indicators.csv' % folder
    with open(path, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            i = Indicator()
            i.index = int(row[0])
            i.id = row[3]
            i.name = row[2]
            i.code = row[3]
            i.unit = row[4]
            i.group = row[5]
            indicators.append(i)
    return indicators


def scale_columns(matrix: numpy.ndarray, v: numpy.ndarray) -> numpy.ndarray:
    result = numpy.zeros(matrix.shape, dtype=numpy.float64)
    for i in range(0, v.shape[0]):
        s = v[i]
        if s == 0:
            continue
        result[:, i] = s * matrix[:, i]
    return result
