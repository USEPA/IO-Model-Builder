import iomb.util as util
import matplotlib.pyplot as plt


class Flow(object):
    def __init__(self, name='', category='', sub_category='', unit=''):
        self.name = name
        self.category = category
        self.subCategory = sub_category
        self.unit = unit
        self.id = util.uuid_of_flow(name, category, sub_category, unit)


class Sector(object):
    def __init__(self, name='', code='', location=''):
        self.name = name
        self.code = code
        self.location = location
        self.id = util.uuid_of_process(name, code, location)


class Table(object):
    def __init__(self):
        self.flows = []
        self.flow_idx = {}
        self.sectors = []
        self.sector_idx = {}
        self.entries = {}

    def add_file(self, csv_file):
        def handle_row(row, i):
            i = self._read_flow(row)
            j = self._read_sector(row)
            val = float(row[8])
            if i not in self.entries:
                self.entries[i] = {}
            self.entries[i][j] = val

        util.each_csv_row(csv_file, handle_row, skip_header=True)

    def _read_flow(self, row) -> int:
        flow = Flow(name=row[0],
                    category=row[2],
                    sub_category=row[3],
                    unit=row[9])
        if flow.id not in self.flow_idx:
            i = len(self.flows)
            self.flows.append(flow)
            self.flow_idx[flow.id] = i
        return self.flow_idx[flow.id]

    def _read_sector(self, row) -> int:
        sector = Sector(name=row[4],
                        code=row[5],
                        location=row[6])
        if sector.id not in self.sector_idx:
            j = len(self.sectors)
            self.sectors.append(sector)
            self.sector_idx[sector.id] = j
        return self.sector_idx[sector.id]

    def viz_flow(self, name):
        idx = None
        for i in range(0, len(self.flows)):
            flow = self.flows[i]
            if flow.name == name:
                idx = i
                break
        if idx is None or idx not in self.entries:
            return
        values = []
        for k, v in self.entries[idx].items():
            values.append(v)
        values.sort()
        plt.bar(range(0, len(values)), values, 1/1.5, color='blue')
        plt.gcf()
        plt.show()
