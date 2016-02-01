"""
imatrix - 2d-numpy arrays decorated with row and column headers.
"""

import csv
import numpy


class IMatrix:
    def __init__(self, row_headers, column_headers):
        self.row_headers = row_headers
        self.column_headers = column_headers
        self.data = numpy.zeros((len(row_headers), len(column_headers)))

    @property
    def row_count(self):
        return len(self.row_headers)

    @property
    def column_count(self):
        return len(self.column_headers)

    def get_row(self, row_header):
        """ Returns the zero-based index of the row with the given header """
        for idx, key in enumerate(self.row_headers):
            if key == row_header:
                return idx
        return -1

    def get_column(self, col_header):
        """ Returns the zero-based index of the column with the given header """
        for idx, key in enumerate(self.column_headers):
            if key == col_header:
                return idx
        return -1

    def get_value(self, row_header, col_header):
        row = self.get_row(row_header)
        col = self.get_column(col_header)
        if row == -1 or col == -1:
            return 0
        return self.data[row, col]

    def set_value(self, row_header, col_header, value):
        row = self.get_row(row_header)
        col = self.get_column(col_header)
        if row == -1 or col == -1:
            return
        self.data[row, col] = value

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


class HeaderIndex:

    def __init__(self, values=[]):
        self.


def read_file(file_path):
    is_dense = False
    row_headers = []
    col_headers = []
    with open(file_path, 'r', newline='\n') as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            row_head = row[0].strip()
            if i == 0 and row_head == '':
                is_dense = True
                for j in range(1, len(row)):
                    col_head = row[j].strip()
                    if col_head not in col_headers:
                        col_headers.append(col_head)
                continue
            if row_head not in row_headers:

            if is_dense:
                pass
            i += 1


