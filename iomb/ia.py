import iomb.refmap as ref
import logging as log
import numpy as np
import pandas as pd
from .util import each_csv_row


class Table(object):
    """ A table with characterization factors of an impact assessment method.
        The factors in the table are index by impact assessment categories in
        the rows and elementary flows in the columns. """

    def __init__(self):
        self.categories = []
        self.category_idx = {}
        self.flows = []
        self.flow_idx = {}
        self.entries = {}

    def add_file(self, csv_file: str):
        """ Reads the given file and adds the entries to this table. """

        def handle_row(row: list, k: int):
            i = self.__read_category(row)
            j = self.__read_flow(row)
            val = float(row[8])
            if i not in self.entries:
                self.entries[i] = {}
            self.entries[i][j] = val

        each_csv_row(csv_file, handle_row, skip_header=True)
        log.info('appended entries from %s to IA table', csv_file)

    def __read_category(self, row: list) -> int:
        category = ref.ImpactCategory.from_ia_row(row)
        key = category.key
        if key not in self.category_idx:
            i = len(self.categories)
            self.categories.append(category)
            self.category_idx[key] = i
            log.info('ia_category[%s]: %s', i, key)
        return self.category_idx[key]

    def __read_flow(self, row: list) -> int:
        flow = ref.ElemFlow.from_ia_row(row)
        key = flow.key
        if key not in self.flow_idx:
            j = len(self.flows)
            self.flows.append(flow)
            self.flow_idx[key] = j
        return self.flow_idx[key]

    def get_factor(self, category: ref.ImpactCategory,
                   flow: ref.ElemFlow) -> float:
        row_idx = self.category_idx.get(category.key)
        col_idx = self.flow_idx.get(flow.key)
        if row_idx is None or col_idx is None:
            return 0.0
        row = self.entries.get(row_idx)
        if row is None:
            return 0.0
        val = row.get(col_idx)
        return 0.0 if val is None else val

    def get_flow(self, flow_key: str) -> ref.ElemFlow:
        """ Returns the flow for the given flow key or None if there is no such
            flow in this impact assessment table. """
        if flow_key is None:
            return None
        idx = self.flow_idx.get(flow_key, -1)
        return None if idx == -1 else self.flows[idx]

    def as_data_frame(self) -> pd.DataFrame:
        rows, cols = len(self.categories), len(self.flows)
        log.info('convert IA table to a %sx%s data frame', rows, cols)
        data = np.zeros((rows, cols), dtype=np.float64)
        for i, row in self.entries.items():
            for j, value in row.items():
                data[i, j] = value
        index = [c.key for c in self.categories]
        columns = [f.key for f in self.flows]
        return pd.DataFrame(data, index=index, columns=columns)
