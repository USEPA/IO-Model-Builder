import csv
import pandas
import random


def weighted_avg(dqis, weights):
    """ An aggregation function that calculates the weighted arithmetic mean of
        the given indicator values and weights. `n.a.`-values are ignored.

        Args:
            dqis (List[int|'n.a.']): the data quality indicators that should be
                aggregated.
            weights (List[float]): the weights of the respective indicators

        Returns:
            the aggregated indicator value.
    """
    length = min(len(dqis), len(weights))
    if length == 0:
        return 'n.a.'
    wsum = 0.0
    max_dqi = -1
    for i in range(0, length):
        dqi = dqis[i]
        if dqi == 'n.a.':
            continue
        wsum += weights[i]
        max_dqi = max(max_dqi, dqi)
    if max_dqi == -1:
        return 'n.a.'
    if wsum == 0.0:
        return max_dqi
    wavg = 0.0
    for i in range(0, length):
        dqi = dqis[i]
        if dqi == 'n.a.':
            continue
        wavg += (dqis[i] * weights[i] / wsum)
    return int(round(wavg))


def aggregate_entries(dqi_entries, weights, aggfn=weighted_avg):
    """ Aggregates all DQI entries using the given weights and aggregation
        function. `None` values in the DQI entries and respective wheights are
        ignored.
    """
    length = min(len(dqi_entries), len(weights))
    if length == 0:
        return []
    e_size = 0
    for dqi_entry in dqi_entries:
        if dqi_entry is not None:
            e_size = max(e_size, len(dqi_entry))
    if e_size == 0:
        return []
    lines = [[] for _ in range(0, e_size)]
    e_weights = []
    for i in range(0, length):
        dqi_entry = dqi_entries[i]
        if dqi_entry is None:
            continue
        e_weights.append(weights[i])
        for pos in range(0, e_size):
            if pos >= len(dqi_entry):
                lines[pos].append('n.a.')
            else:
                lines[pos].append(dqi_entry[pos])
    agg_entry = []
    for line in lines:
        agg_entry.append(aggfn(line, e_weights))
    return agg_entry


class Entry(object):

    @staticmethod
    def to_string(val):
        if val is None:
            return '(none)'
        vs = '('
        for i in range(0, len(val)):
            vs += '%s' % val[i]
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
            v = val.strip()
            if v == 'n.a.':
                e.append(v)
            else:
                e.append(int(v))
        return e


class Matrix(object):

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
        if not isinstance(other, Matrix):
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
            return Matrix(len(v_rows), 0)
        m = Matrix(len(v_rows), len(v_rows[0]))
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

    def to_string_list(self):
        """ Returns the data of this matrix as 2-dimensional list where each
            DQI entry is converted to a string."""
        rows = [None] * self.rows
        for row in range(0, self.rows):
            vals = [None] * self.cols
            rows[row] = vals
            for col in range(0, self.cols):
                vals[col] = Entry.to_string(self[row, col])
        return rows

    @staticmethod
    def from_csv(file_name: str):
        with open(file_name, 'r', encoding='utf-8', newline='\n') as f:
            reader = csv.reader(f)
            rows = []
            for line in reader:
                rows.append([Entry.from_string(e) for e in line])
            if len(rows) == 0:
                return Matrix(0, 0)
            m = Matrix(len(rows), len(rows[0]))
            for row_idx in range(0, m.rows):
                row = rows[row_idx]
                for col_idx in range(0, len(row)):
                    m[row_idx, col_idx] = row[col_idx]
            return m

    @staticmethod
    def from_sat_table(model):
        """ Creates the DQI matrix of the satellite table of the given model.
            The rows (flows) and columns (sectors) are aligned as in the data
            frames of the calculation.
        """
        A = model.drc_matrix
        B = model.sat_table.as_data_frame().reindex(
            columns=A.index, fill_value=0.0)
        rows, cols = B.shape
        m = Matrix(rows, cols)
        for row in range(0, m.rows):
            for col in range(0, m.cols):
                flow_key = B.index[row]
                sector_key = A.index[col]
                e = model.sat_table.get_entry(flow_key, sector_key)
                if e is None or not isinstance(e.data_quality_entry, str):
                    m[row, col] = None
                    continue
                sat_dq = e.data_quality_entry.strip()
                sat_dq = sat_dq[1: len(sat_dq) - 1]
                e = []
                for i in sat_dq.split(';'):
                    val = i.strip()
                    if val != 'n.a.':
                        val = int(val)
                    e.append(val)
                m[row, col] = e
        return m

    @staticmethod
    def rand(rows: int, cols: int, tsize=5, mini=1, maxi=5):
        m = Matrix(rows, cols)
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
        r = Matrix(self.rows, 1)
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
        r = Matrix(m, n)
        for row_A in range(0, m):
            for col_B in range(0, n):
                weights = []
                for i in range(0, k):
                    weights.append(A[row_A][i] * B[i][col_B])
                entries = self.get_row(row_A) if left else self.get_col(col_B)
                agg_entry = aggregate_entries(entries, weights, aggfn)
                r[row_A, col_B] = agg_entry
        return r
