"""
imatrix - 2d-numpy arrays decorated with row and column headers.
"""

import csv
import numpy


class IMatrix:
    def __init__(self, row_idx, col_idx):
        self.row_idx = Index(row_idx) if type(row_idx) is list else row_idx
        self.col_idx = Index(col_idx) if type(col_idx) is list else col_idx
        self.data = numpy.zeros((len(row_idx), len(col_idx)))

    @property
    def row_count(self):
        return len(self.row_idx)

    @property
    def column_count(self):
        return len(self.col_idx)

    def get_row(self, row_header):
        """ Returns the zero-based index of the row with the given header """
        return self.row_idx.get_idx(row_header)

    def get_column(self, col_header):
        """ Returns the zero-based index of the column with the given header """
        return self.col_idx.get_idx(col_header)

    def get(self, row_header, col_header):
        row = self.get_row(row_header)
        col = self.get_column(col_header)
        if row == -1 or col == -1:
            return 0
        return self.data[row, col]

    def __getitem__(self, cell_headers):
        row_header, col_header = cell_headers
        return self.get(row_header, col_header)

    def set(self, row_header, col_header, value):
        row = self.get_row(row_header)
        col = self.get_column(col_header)
        if row == -1 or col == -1:
            return
        self.data[row, col] = value

    def __setitem__(self, cell_headers, value):
        row_header, col_header = cell_headers
        self.set(row_header, col_header, value)

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

    def write_dense(self, file_path):
        row_keys = []
        row_keys.extend(self.row_idx.headers)
        row_keys.sort()
        col_keys = []
        col_keys.extend(self.col_idx.headers)
        col_keys.sort()
        with open(file_path, 'w', newline='\n') as f:
            writer = csv.writer(f)
            headers = ['']
            headers.extend(col_keys)
            writer.writerow(headers)
            for row_key in row_keys:
                entries = [row_key]
                for col_key in col_keys:
                    entries.append(self.get(row_key, col_key))
                writer.writerow(entries)

    def write_sparse(self, file_path):
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


class Index:

    def __init__(self, headers=[]):
        self.headers = headers
        self.idx_map = {}
        for header in headers:
            self.idx_map[header] = len(self.idx_map)

    def get_idx(self, header):
        """
        Get the matrix index of the given header or -1 if the given header is
        not contained in this index.
        """
        return self.idx_map[header] if header in self.idx_map else -1

    def get_header(self, idx):
        """ Get the header at the given index. """
        if idx < 0 or idx > (len(self.headers) - 1):
            return None
        else:
            return self.headers[idx]

    def __len__(self):
        return len(self.headers)


def read_file(file_path):
    matrix, is_dense = __parse_shape(file_path)
    col_idx = {}
    i = -1
    for row in __rows(file_path):
        i += 1
        if i == 0 and is_dense:
            for j in range(1, len(row)):
                col_head = row[j].strip()
                col_idx[j] = col_head
            continue
        row_head = row[0].strip()
        if is_dense:
            for j in range(1, len(row)):
                val_str = row[j].strip()
                if val_str == '':
                    continue
                col_head = col_idx[j]
                matrix.set(row_head, col_head, float(val_str))
        else:
            col_head = row[1].strip()
            val_str = row[2].strip()
            if val_str != '':
                matrix.set(row_head, col_head, float(val_str))
    return matrix


def __parse_shape(file_path):
    row_headers = []
    col_headers = []
    is_dense = False
    i = -1
    for row in __rows(file_path):
        i += 1
        row_head = row[0].strip()
        if i == 0 and row_head == '':
            is_dense = True
            for j in range(1, len(row)):
                col_head = row[j].strip()
                if col_head not in col_headers:
                    col_headers.append(col_head)
            continue
        if row_head not in row_headers:
            row_headers.append(row_head)
        if is_dense:
            continue
        col_head = row[1].strip()
        if col_head not in col_headers:
            col_headers.append(col_head)
    row_headers.sort()
    col_headers.sort()
    return IMatrix(row_headers, col_headers), is_dense


def __rows(file_path):
    with open(file_path, 'r', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row
