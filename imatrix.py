"""
imatrix - 2d-numpy arrays decorated with row and column indices
"""

import csv
import numpy


class IMatrix:
    def __init__(self, row_index, column_index):
        self.row_index = row_index
        self.column_index = column_index
        self.data = numpy.zeros((len(row_index), len(column_index)))

    @property
    def row_count(self):
        return len(self.row_index)

    @property
    def column_count(self):
        return len(self.column_index)

    def get_row(self, row_key):
        """ Returns the zero-based index of the row with the given key """
        for idx, key in enumerate(self.row_index):
            if key == row_key:
                return idx
        return -1

    def get_column(self, col_key):
        """ Returns the zero-based index of the column with the given key """



    def add_entry(self, row_key, col_key, value):
        if value is None:
            return 0
        v = float(value)
        row = self.add_row(row_key)
        col = self.add_col(col_key)
        if row not in self.values:
            self.values[row] = {}
        self.values[row][col] = v
        return v

    def get_row_key(self, row):
        for key in self.row_idx:
            if self.row_idx[key] == row:
                return key
        return None

    def get_col_key(self, col):
        for key in self.col_idx:
            if self.col_idx[key] == col:
                return key
        return None

    def get_entry(self, row, col):
        r = row
        c = col
        if type(row) == str:
            r = self.row_idx[row] if row in self.row_idx else None
            c = self.col_idx[col] if col in self.col_idx else None
        if r is None or c is None:
            return 0
        if r not in self.values:
            return 0
        row_entries = self.values[r]
        if c not in row_entries:
            return 0
        val = row_entries[c]
        return 0 if val is None else val

    def get_col_sums(self):
        sums = {}
        for col_key in self.col_keys:
            col_sum = 0
            for row_key in self.row_keys:
                val = self.get_entry(row_key, col_key)
                col_sum += val
            sums[col_key] = col_sum
        return sums

    def get_row_sums(self):
        sums = {}
        for row_key in self.row_keys:
            row_sum = 0
            for col_key in self.col_keys:
                val = self.get_entry(row_key, col_key)
                row_sum += val
            sums[row_key] = row_sum
        return sums

    def entries(self):
        for row_key in self.row_keys:
            for col_key in self.col_keys:
                val = self.get_entry(row_key, col_key)
                if val != 0:
                    yield (row_key, col_key, val)

    def mult(self, other):
        result = IMatrix()
        for row_key in self.row_keys:
            for col_key in other.col_keys:
                val = 0
                for i in self.col_keys:
                    val += self.get_entry(row_key, i) * other.get_entry(i,
                                                                        col_key)
                result.add_entry(row_key, col_key, val)
        return result

    def filter(self, row_keys, col_keys):
        """
        Returns a new matrix which contains only entries with the given row and
        column keys.
        :param row_keys: The row keys that should be contained in the new
                matrix.
        :param col_keys: The column keys that should be contained in the new
                matrix.
        :return: A new matrix.
        """
        m = IMatrix()
        for entry in self.entries():
            row_key = entry[0]
            col_key = entry[1]
            if row_key in row_keys and col_key in col_keys:
                m.add_entry(row_key, col_key, entry[2])
        return m

    def write_dense_csv(self, file_path, delimiter=','):
        row_keys = []
        row_keys.extend(self.row_keys)
        row_keys.sort()
        col_keys = []
        col_keys.extend(self.col_keys)
        col_keys.sort()
        with open(file_path, 'w', newline='\n') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC,
                                delimiter=delimiter)
            headers = ['']
            headers.extend(col_keys)
            writer.writerow(headers)
            for row_key in row_keys:
                entries = [row_key]
                for col_key in col_keys:
                    entries.append(self.get_entry(row_key, col_key))
                writer.writerow(entries)

    def write_sparse_csv(self, file_path):
        row_keys = [r for r in self.row_keys]
        row_keys.sort()
        col_keys = [c for c in self.col_keys]
        col_keys.sort()
        with open(file_path, 'w', newline='\n') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
            first_row = True  # write each row and column key at least once
            for row in row_keys:
                first_col = True
                for col in col_keys:
                    val = self.get_entry(row, col)
                    should_write = first_row or first_col
                    if val == 0 and not should_write:
                        continue
                    writer.writerow([row, col, val])
                    first_col = False
                first_row = False


def read_sparse_csv(file_path):
    m = IMatrix()
    with open(file_path, 'r', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            m.add_entry(row[0], row[1], row[2])
    return m
