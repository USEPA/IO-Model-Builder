import iomb.util as util
import matplotlib.pyplot as plt
import iomb.model as model
import pandas as pd
import numpy as np


class Table(object):
    def __init__(self):
        self.flows = []
        self.flow_idx = {}
        self.sectors = []
        self.sector_idx = {}
        self.entries = {}

    def add_file(self, csv_file: str):
        """ Reads the given CSV file and adds the entries to this satellite
            table.
        """

        def handle_row(row, i):
            i = self._read_flow(row)
            j = self._read_sector(row)
            val = float(row[8])
            if i not in self.entries:
                self.entries[i] = {}
            self.entries[i][j] = val

        util.each_csv_row(csv_file, handle_row, skip_header=True)

    def _read_flow(self, row) -> int:
        flow = model.ElemFlow(name=row[0], category=row[2], sub_category=row[3],
                              uid=row[4], unit=row[9])
        if flow.uid not in self.flow_idx:
            i = len(self.flows)
            self.flows.append(flow)
            self.flow_idx[flow.uid] = i
        return self.flow_idx[flow.uid]

    def _read_sector(self, row) -> int:
        sector = model.Sector(name=row[5],
                              code=row[6],
                              location=row[7])
        if sector.uid not in self.sector_idx:
            j = len(self.sectors)
            self.sectors.append(sector)
            self.sector_idx[sector.uid] = j
        return self.sector_idx[sector.uid]

    def as_data_frame(self) -> pd.DataFrame:
        """ Converts the satellite table into a pandas data frame where the
            row index contains the keys of the elementary flows, the column
            index the keys of the commodity sectors, and the values the amounts
            of the elementary flows for the respective sectors.
        """
        rows, cols = len(self.flows), len(self.sectors)
        data = np.zeros((rows, cols), dtype=np.float64)
        for i, row in self.entries.items():
            for j, val in row.items():
                data[i, j] = val
        index = [f.key for f in self.flows]
        columns = [s.key for s in self.sectors]
        return pd.DataFrame(data=data, index=index, columns=columns)

    def viz_flow(self, name):
        idx = None
        flow = None
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
        plt.hist(values, 30, color='blue')
        plt.title(name)
        plt.xlabel(flow.unit + ' / USD')
        plt.ylabel('Absolute frequency')
        plt.show()
