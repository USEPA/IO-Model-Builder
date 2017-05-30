import csv
import random


def weighted_avg(dqis, weights) -> int:
    """ An aggregation function that calculates the weighted arithmetic mean of
        the given indicator values and weights.

        Args:
            dqis (List[int]): the data quality indicators that should be
                aggregated.
            weights (List[float]): the weights of the respective indicators

        Returns:
            the aggregated indicator value.
    """
    length = min(len(dqis), len(weights))
    if length == 0:
        return 0
    wsum = 0.0
    max_dqi = 0
    for i in range(0, length):
        wsum += weights[i]
        max_dqi = max(max_dqi, dqis[i])
    if wsum == 0.0:
        return max_dqi
    wavg = 0.0
    for i in range(0, length):
        wavg += (dqis[i] * weights[i] / wsum)
    return int(round(wavg))


def aggregate_entries(dqi_entries, weights, aggfn=weighted_avg):
    """ Aggregates all DQI entries using the given weights and aggregation
        function.
    """
    length = min(len(dqi_entries), len(weights))
    if length == 0:
        return []
    e_size = len(dqi_entries[0])
    lines = [[] for _ in range(0, e_size)]
    for dqi_entry in dqi_entries:
        if dqi_entry is None:
            for i in range(0, e_size):
                lines[i].append(0)
        for pos in range(0, e_size):
            lines[pos].append(dqi_entry[pos])
    agg_entry = []
    for line in lines:
        agg_entry.append(aggfn(line, weights))
    return agg_entry


class Entry(object):

    @staticmethod
    def to_string(val):
        if val is None:
            return '(none)'
        vs = '('
        for i in range(0, len(val)):
            vs += '%i' % val[i]
            if i < (len(val) - 1):
                vs += ','
        vs += ')'
        return vs

    @staticmethod
    def from_string(s: str):
        if s is None:
            return None
        vals = s.strip().strip('()').split(',')
        if len(vals) == 0 or vals[0] == 'none':
            return None
        e = []
        for val in vals:
            e.append(int(val))
        return e


class DqiMatrix(object):

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.data = [None] * (rows * cols)

    def __idx__(self, row, col):
        return row + self.rows * col

    def __getitem__(self, idx):
        row, col = idx
        i = self.__idx__(row, col)
        return self.data[i]

    def __setitem__(self, idx, value):
        row, col = idx
        i = self.__idx__(row, col)
        self.data[i] = value

    def get_row(self, idx):
        row = []
        for col in range(0, self.cols):
            row.append(self[idx, col])
        return row

    def get_col(self, idx):
        col = []
        for row in range(0, self.rows):
            col.append(self[row, idx])
        return col

    def __str__(self):
        s = "["
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                val = self[row, col]
                s += ' ' + Entry.to_string(val)
            if row < (self.rows - 1):
                s += ' ;\n '
            else:
                s += ' ]'
        return s

    def __eq__(self, other):
        if not isinstance(other, DqiMatrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return self.data == other.data

    @staticmethod
    def parse(s: str):
        if s is None:
            return None
        t = s.strip().strip('[]')
        ''.split()
        t_rows = t.split(';')
        v_rows = []
        for t_row in t_rows:
            v_row = []
            v_rows.append(v_row)
            t_entries = t_row.strip().strip('()').split(')')
            for t_entry in t_entries:
                entry = Entry.from_string(t_entry)
                v_row.append(entry)
        if len(v_rows) == 0 or len(v_rows[0]) == 0:
            return DqiMatrix(len(v_rows), 0)
        m = DqiMatrix(len(v_rows), len(v_rows[0]))
        for row in range(0, m.rows):
            for col in range(0, m.cols):
                m[row, col] = v_rows[row][col]
        return m

    def to_csv(self, file_name: str):
        with open(file_name, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            for row in range(0, self.rows):
                csv_row = [Entry.to_string(self[row, col])
                           for col in range(0, self.cols)]
                writer.writerow(csv_row)

    @staticmethod
    def rand(rows: int, cols: int, tsize=5, mini=1, maxi=5):
        m = DqiMatrix(rows, cols)
        for row in range(0, rows):
            for col in range(0, cols):
                t = [None] * tsize
                m[row, col] = t
                for i in range(0, tsize):
                    t[i] = random.randint(mini, maxi)
        return m

    def aggregate_columns(self, base_matrix, factors=None, aggfn=weighted_avg):
        """ Aggregates the columns of the DQI matrix using the values from
            the given corresponding base matrix.

            Args:
                base_matrix: a matrix with the corresponding numeric values
                    (must have the same shape as the DQI matrix).
                factors: an optional vector with colum factors that should be
                    applied (if given, the length of this vector needs to be
                    equal to the column dimension of the base matrix).
                aggfn: the aggregation function for the data quality
                    indicators; defaults to weighted_avg.

            Returns:
                an aggregated DQI matrix with one column and the same number of
                rows as the original matrix.
        """
        r = DqiMatrix(self.rows, 1)
        for row in range(0, self.rows):
            weights = [0.0] * self.cols
            for col in range(0, self.cols):
                weight = base_matrix[row][col]
                if factors is not None:
                    weight *= factors[col]
                weights[col] = weight
            entries = self.get_row(row)
            r[row, 0] = aggregate_entries(entries, weights, aggfn)
        return r

    def aggregate_mmult(self, A, B, left=True, aggfn=weighted_avg):
        """ Aggregates the DQI matrix within a matrix-matrix multiplication.

            Args:
                A: the left m*k matrix of the multiplication
                B: the right k*n matrix of the multiplication
                left: indicates whether the left matrix (default; True) or the
                    right matrix is the base-matrix of the DQI matrix.
                aggfn: the aggregation function for the data quality
                    indicators; defaults to weighted_avg.

            Returns:
                a m*n matrix with aggregated DQI values
        """
        m = len(A)
        k = len(B)
        n = len(B[0])
        r = DqiMatrix(m, n)
        for row_A in range(0, m):
            for col_B in range(0, n):
                weights = []
                for i in range(0, k):
                    weights.append(A[row_A][i] * B[i][col_B])
                entries = self.get_row(row_A) if left else self.get_col(col_B)
                agg_entry = aggregate_entries(entries, weights, aggfn)
                r[row_A, col_B] = agg_entry
        return r
