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
        self.comment = None  # type: str
        # TODO: add uncertainty information

    @staticmethod
    def from_csv(csv_row):
        val = float(csv_row[8])
        e = Entry(val)
        e.data_quality_entry = Entry.__read_dq_values(csv_row)
        e.comment = Entry.__read_comment(csv_row)
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
    def __read_comment(csv_row):

        def add_entry(header: str, row: list, idx: int, comment: str) -> str:
            val = util.csv_val(row, idx)
            if val is None or not isinstance(val, str):
                return
            val = val.strip()
            if val == '':
                return
            entry = '%s: %s' % (header, val)
            if comment is not None:
                comment += ('; ' + entry)
            else:
                comment = entry
            return comment

        comment = add_entry('Data year', csv_row, 20, None)
        comment = add_entry('Tags', csv_row, 21, comment)
        comment = add_entry('Sources', csv_row, 22, comment)
        comment = add_entry('Other', csv_row, 23, comment)
        return comment

    @staticmethod
    def empty():
        return Entry(0.0)

    def to_csv(self, flow: ref.ElemFlow, sector: ref.Sector) -> list:
        """ Converts the satellite matrix entry to a CSV row. """
        dq = Entry.__split_dq_entry(self.data_quality_entry)
        if dq is None:
            dq = [None, None, None, None, None]
        return [flow.name, flow.cas_number, flow.category, flow.sub_category,
                flow.uid, sector.name, sector.code, sector.location,
                self.value, flow.unit, None, None, None, None, None,
                dq[0], dq[1], dq[2], dq[3], dq[4]]

    def copy(self):
        c = Entry(self.value)
        c.data_quality_entry = self.data_quality_entry
        c.comment = self.comment
        return c

    def add(self, value: float, data_quality_entry=None, comment=None):
        """ Adds the given value to this satellite matrix entry. """
        self.__add_dq(value, data_quality_entry)
        self.value += value
        if comment is not None:
            if self.comment is None:
                self.comment = comment
            else:
                c = self.comment + '\n\n' + comment
                if len(c) < 100000:  # ~ openLCA limit
                    self.comment = c

    def __add_dq(self, value: float, data_quality_entry=None):
        self_dq = Entry.__split_dq_entry(self.data_quality_entry)
        other_dq = Entry.__split_dq_entry(data_quality_entry)
        if other_dq is None or value is None or value == 0:
            return
        if self_dq is None:
            self.data_quality_entry = data_quality_entry
            return
        new_entries = []
        for i in range(0, 5):
            sdq_i, odq_i = 0, 0
            try:
                sdq_i = int(self_dq[i])
            except ValueError:
                sdq_i = 'n.a.'
            try:
                odq_i = int(other_dq[i])
            except ValueError:
                odq_i = 'n.a.'
            if sdq_i == 'n.a.':
                new_entries.append(odq_i)
            elif odq_i == 'n.a.':
                new_entries.append(sdq_i)
            else:
                val = (sdq_i * self.value + odq_i * value) / (self.value + value)
                new_entries.append(int(round(val)))
        new_entries = [str(x) for x in new_entries]
        self.data_quality_entry = '(' + ';'.join(new_entries) + ')'

    @staticmethod
    def __split_dq_entry(dq_entry: str):
        if not isinstance(dq_entry, str):
            return None
        sub = dq_entry.strip()[1: len(dq_entry) - 1]
        dq = [q for q in sub.split(';')]
        return None if len(dq) < 5 else dq


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
            new_entry = Entry.from_csv(row)
            row_map = self.entries.get(i)
            if row_map is None:
                row_map = {}
                self.entries[i] = row_map
            old_entry = row_map.get(j)  # type: Entry
            if old_entry is None:
                row_map[j] = new_entry
            else:
                old_entry.add(new_entry.value, new_entry.data_quality_entry,
                              new_entry.comment)

        util.each_csv_row(csv_file, handle_row, skip_header=True)
        log.info('appended entries from %s to satellite table', csv_file)
        log.info('satellite table contains %s flows and %s sectors',
                 len(self.flows), len(self.sectors))

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

    def get_flow(self, flow_key: str) -> ref.ElemFlow:
        """ Returns the flow for the given flow key or None if there is no such
            flow in this satellite table. """
        if flow_key is None:
            return None
        idx = self.flow_idx.get(flow_key, -1)
        return None if idx == -1 else self.flows[idx]

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

    def apply_market_shares(self, market_shares: pd.DataFrame,
                            sector_info_csv: str):
        """ Applies the given market share matrix (industries x commodities) to
            this satellite table. It returns a new satellite table with the same
            flow index but with a commodity sector index that matches the
            columns from the market shares with the given meta-information. """
        log.info("apply market shares ...")
        new_table = Table()
        new_table.flows = self.flows
        new_table.flow_idx = self.flow_idx
        sector_info = ref.SectorMap.read(sector_info_csv)
        new_table.entries = {}

        log.info("   ... map shares")
        shares = {}
        for commodity in market_shares.columns:
            new_sector = sector_info.get(commodity)
            if new_sector is None:
                log.error('commodity sector %s is not contained in %s: ignored',
                          commodity, sector_info_csv)
                continue
            new_col = len(new_table.sectors)
            new_table.sectors.append(new_sector)
            new_table.sector_idx[new_sector.key] = new_col
            share_entries = {}
            shares[new_col] = share_entries
            m_shares = market_shares.ix[:, commodity]
            for industry_key in m_shares.index:
                share = m_shares[industry_key]
                if share == 0:
                    continue
                old_col = self.sector_idx.get(industry_key)
                if old_col is not None:
                    share_entries[old_col] = share

        log.info("   ... apply shares")
        for flow in self.flows:
            row_idx = self.flow_idx.get(flow.key, -1)
            old_row = self.entries.get(row_idx)
            if old_row is None:
                continue  # no entries for the flow
            new_row = {}
            new_table.entries[row_idx] = new_row
            for new_col, m_shares in shares.items():
                new_entry = None
                for old_col, old_entry in old_row.items():
                    share = m_shares.get(old_col, 0)
                    if share == 0:
                        continue
                    value = share * old_entry.value
                    if new_entry is None:
                        new_entry = old_entry.copy()
                        new_entry.value = value
                    else:
                        new_entry.add(value, old_entry.data_quality_entry,
                                      old_entry.comment)
                if new_entry is None:
                    continue
                new_row[new_col] = new_entry

        return new_table
