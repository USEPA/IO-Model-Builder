import csv
import json
import os

import iomb.dqi as dqi
import iomb.matio as matio


class Sector(object):

    def __init__(self):
        self.id = ''
        self.index = 0
        self.name = ''
        self.code = ''
        self.location = ''

    def as_json_dict(self):
        return {
            'id': self.id,
            'index': self.index,
            'name': self.name,
            'code': self.code,
            'location': self.location
        }


class Indicator(object):

    def __init__(self):
        self.id = ''
        self.index = 0
        self.name = ''
        self.code = ''
        self.unit = ''

    def as_json_dict(self):
        return {
            'id': self.id,
            'index': self.index,
            'name': self.name,
            'code': self.code,
            'unit': self.unit
        }


class Model(object):

    def __init__(self, folder: str):
        self.folder = folder
        self.sectors = read_sectors(folder)
        self.indicators = read_indicators(folder)  # type: list[Indicator]
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
        m = dqi.Matrix.from_csv(path)
        self.matrix_cache[name] = m
        return m


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
            indicators.append(i)
    indicators.sort(key=lambda i: i.index)
    return indicators
