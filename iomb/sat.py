import csv
import iomb.util as util
import iomb.refmap as ref
import logging as log
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Entry(object):
    """ Contains the information of an entry in a satellite table. """

    def __init__(self, value: float):
        self.value = value
        self.data_quality_entry = None
        # TODO: add uncertainty information

    @staticmethod
    def from_csv(csv_row):
        val = float(csv_row[8])
        e = Entry(val)
        e.data_quality_entry = Entry.__read_dq_values(csv_row)
        return e

    @staticmethod
    def __read_dq_values(csv_row):
        if len(csv_row) < 20:
            return None
        raw = csv_row[15:20]
        dq_values = []
        all_empty = True
        for v in raw:
            if v is None or v == '':
                dq_values.append('n.a.')
                continue
            all_empty = False
            dq_values.append(v)
        if all_empty:
            return None
        else:
            return '(' + ';'.join(dq_values) + ')'

    @staticmethod
    def empty():
        return Entry(0.0)

    def to_csv(self, flow: ref.ElemFlow, sector: ref.Sector) -> list:
        """ Converts the satellite matrix entry to a CSV row. """
        dq = None
        if self.data_quality_entry is None:
            dq = [None, None, None, None, None]
        else:
            s = self.data_quality_entry[1: len(self.data_quality_entry) - 1]
            dq = [q for q in s.split(';')]
            dq = dq if len(dq) >= 5 else [None, None, None, None, None]
        return [flow.name, flow.cas_number, flow.category, flow.sub_category,
                flow.uid, sector.name, sector.code, sector.location,
                self.value, flow.unit, None, None, None, None, None,
                dq[0], dq[1], dq[2], dq[3], dq[4]]


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

        def handle_row(row, _):
            i = self.__read_flow(row)
            j = self.__read_sector(row)
            entry = Entry.from_csv(row)
            if i not in self.entries:
                self.entries[i] = {}
            self.entries[i][j] = entry

        util.each_csv_row(csv_file, handle_row, skip_header=True)
        log.info('appended entries from %s to satellite table', csv_file)

    def __read_flow(self, row) -> int:
        flow = ref.ElemFlow.from_satellite_row(row)
        key = flow.key
        if key not in self.flow_idx:
            i = len(self.flows)
            self.flows.append(flow)
            self.flow_idx[key] = i
            log.debug('add satellite flow[%s]: %s', i, key)
        return self.flow_idx[key]

    def __read_sector(self, row) -> int:
        sector = ref.Sector.from_satellite_row(row)
        key = sector.key
        if key not in self.sector_idx:
            j = len(self.sectors)
            self.sectors.append(sector)
            self.sector_idx[key] = j
        return self.sector_idx[key]

    def get_entry(self, flow_key: str, sector_key: str) -> Entry:
        row = self.flow_idx.get(flow_key, -1)
        if row == -1:
            log.warning('flow %s is not in the satellite table', flow_key)
            return Entry.empty()
        col = self.sector_idx.get(sector_key, -1)
        if col == -1:
            log.warning('sector %s is not in the satellite table', sector_key)
            return Entry.empty()
        row_entries = self.entries.get(row, None)
        if row_entries is None:
            return Entry.empty()
        return row_entries.get(col, Entry.empty())

    def as_data_frame(self) -> pd.DataFrame:
        """ Converts the satellite table into a pandas data frame where the
            row index contains the keys of the elementary flows, the column
            index the keys of the commodity sectors, and the values the amounts
            of the elementary flows for the respective sectors.
        """
        rows, cols = len(self.flows), len(self.sectors)
        log.info('convert satellite table to a %sx%s data frame', rows, cols)
        data = np.zeros((rows, cols), dtype=np.float64)
        for i, row in self.entries.items():
            for j, entry in row.items():
                data[i, j] = entry.value
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
        for k, e in self.entries[idx].items():
            values.append(e.value)
        values.sort()
        plt.hist(values, 30, color='blue')
        plt.title(name)
        plt.xlabel(flow.unit + ' / USD')
        plt.ylabel('Absolute frequency')
        plt.show()

    def to_csv(self, file_name: str):
        """ Writes the satellite matrix to a CSV file. """
        header = ['Flow name', 'CAS number', 'Category', 'Sub-category',
                  'Flow UUID', 'Sector name', 'Sector code', 'Sector location',
                  'Amount', 'Unit', 'Distribution type', 'Expected value',
                  'Dispersion', 'Minimum', 'Maximum', 'Reliability',
                  'Temporal correlation', 'Geographical correlation',
                  'Technological correlation', 'Data collection']
        log.info('write satellite table to %s', file_name)
        with open(file_name, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for flow in self.flows:
                row_idx = self.flow_idx.get(flow.key, -1)
                if row_idx == -1:
                    log.warning('flow %s is not contained in flow index', flow)
                    continue
                row = self.entries.get(row_idx)
                if row is None:
                    log.warning('no satellite entries for flow %s', flow)
                    continue
                for sector in self.sectors:
                    col = self.sector_idx.get(sector.key, -1)
                    if col == -1:
                        continue
                    entry = row.get(col)
                    if entry is None:
                        continue
                    writer.writerow(entry.to_csv(flow, sector))
