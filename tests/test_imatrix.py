import imatrix
import unittest


class TestIMatrixMethods(unittest.TestCase):

    def test_size(self):
        m = imatrix.IMatrix(['r1', 'r2', 'r3'], ['c1', 'c2'])
        self.assertEqual(3, m.row_count)
        self.assertEqual(2, m.column_count)

    def test_header_methods(self):
        m = imatrix.IMatrix(['r1', 'r2', 'r3'], ['c1', 'c2'])
        self.assertEqual(2, m.get_row('r3'))
        self.assertEqual(1, m.get_column('c2'))
        m.set_value('r1', 'c1', 42)
        self.assertEqual(42, m.data[0, 0])
        self.assertEqual(42, m.get_value('r1', 'c1'))

if __name__ == '__main__':
    unittest.main()
