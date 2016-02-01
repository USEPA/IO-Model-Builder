import imatrix
import unittest


class TestIMatrixMethods(unittest.TestCase):

    def test_size(self):
        m = imatrix.IMatrix(['r1', 'r2', 'r3'], ['c1', 'c2'])
        self.assertEqual(3, m.row_count)
        self.assertEqual(2, m.column_count)

if __name__ == '__main__':
    unittest.main()
