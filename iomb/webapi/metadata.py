import csv
import json


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
    path = '%s/lcia-categories.csv' % folder
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
    indicators.sort(key i: i.index)
    return indicators
