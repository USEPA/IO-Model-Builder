import random


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

    def __str__(self):
        s = "["
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                val = self[row, col]
                if val is None:
                    s += ' (none)'
                    continue
                vs = ' ('
                for i in range(0, len(val)):
                    vs += '%i' % val[i]
                    if i < (len(val) - 1):
                        vs += ','
                vs += ')'
                s += vs
            if row < (self.rows - 1):
                s += ' ;\n  '
            else:
                s += ' ]'
        return s

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
                vals = t_entry.strip().strip('()').split(',')
                if len(vals) == 0 or vals[0] == 'none':
                    v_row.append(None)
                    continue
                e = []
                v_row.append(e)
                for val in vals:
                    e.append(int(val))
        if len(v_rows) == 0 or len(v_rows[0]) == 0:
            return DqiMatrix(len(v_rows), 0)
        m = DqiMatrix(len(v_rows), len(v_rows[0]))
        for row in range(0, m.rows):
            for col in range(0, m.cols):
                m[row, col] = v_rows[row][col]
        return m

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
