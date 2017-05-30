import unittest
import iomb.dqi as dqi


class TestDqiMatrix(unittest.TestCase):

    def test_indices(self):
        m = dqi.DqiMatrix(3, 5)
        m[2, 4] = (1, 2, 3, 4, 5)
        self.assertEqual((1, 2, 3, 4, 5), m[2, 4])

    def test_rand(self):
        m = dqi.DqiMatrix.rand(5, 10)
        for row in range(0, m.rows):
            for col in range(0, m.cols):
                val = m[row, col]
                self.assertTrue(isinstance(val, list))
                self.assertEqual(5, len(val))
                for i in range(0, len(val)):
                    self.assertTrue(isinstance(val[i], int))

    def test_parse(self):
        t = """
        [ (1,2,4) (3,3,2) (4,2,2) ;
          (4,2,4) (none)  (5,2,5) ]
        """
        m = dqi.DqiMatrix.parse(t)
        # print(m)
        self.assertEqual([1, 2, 4], m[0, 0])
        self.assertEqual([3, 3, 2], m[0, 1])
        self.assertEqual([4, 2, 2], m[0, 2])
        self.assertEqual([4, 2, 4], m[1, 0])
        self.assertEqual(None, m[1, 1])
        self.assertEqual([5, 2, 5], m[1, 2])

    def test_eq(self):
        t = """
        [ (1,2,4) (3,3,2) (4,2,2) ;
          (4,2,4) (none)  (5,2,5) ]
        """
        m1 = dqi.DqiMatrix.parse(t)
        m2 = dqi.DqiMatrix.parse(t)
        self.assertEqual(m1, m2)
        t = """
        [ (2,2,4) (3,3,2) (4,2,2) ;
          (4,2,4) (none)  (5,2,5) ]
        """
        m3 = dqi.DqiMatrix.parse(t)
        self.assertNotEqual(m1, m3)


class TestAggregation(unittest.TestCase):

    def test_weighted_avg(self):
        self.assertEqual(0, dqi.weighted_avg([], []))
        self.assertEqual(5, dqi.weighted_avg([5], [0.3]))
        self.assertEqual(3, dqi.weighted_avg([5, 3, 2], [0.3, 0.8, 0.1]))

    def test_aggregate_entries(self):
        entries = [[4, 1, 3], [2, 1, 5]]
        weights = [0.4,  0.7]
        agg_entry = dqi.aggregate_entries(entries, weights)
        self.assertEqual([3, 1, 4], agg_entry)

    def test_aggregate_columns(self):
        t = """
            [ (4,1,3) (2,1,5) ;
              (4,5,3) (1,5,1) ;
              (2,1,5) (3,1,4) ]
        """
        m = dqi.DqiMatrix.parse(t)
        base = [[0.4,  0.7],
                [0.1,  0.5],
                [0.9,  0.2]]
        r = m.aggregate_columns(base)
        self.assertEqual(3, r.rows)
        self.assertEqual(1, r.cols)
        self.assertEqual([3, 1, 4], r[0, 0])
        self.assertEqual([2, 5, 1], r[1, 0])
        self.assertEqual([2, 1, 5], r[2, 0])

    def test_aggregate_columns_with_factors(self):
        t = """
            [ (4,1,3) (2,1,5) ;
              (4,5,3) (1,5,1) ;
              (2,1,5) (3,1,4) ]
        """
        m = dqi.DqiMatrix.parse(t)
        base = [[0.4,  0.7],
                [0.1,  0.5],
                [0.9,  0.2]]
        factors = [0.7, 0.3]
        r = m.aggregate_columns(base, factors)
        self.assertEqual(3, r.rows)
        self.assertEqual(1, r.cols)
        self.assertEqual([3, 1, 4], r[0, 0])
        self.assertEqual([2, 5, 2], r[1, 0])
        self.assertEqual([2, 1, 5], r[2, 0])

    def test_aggregate_mmult_left(self):
        t = """
            [ (4,1,3) (2,1,5) ;
              (4,5,3) (1,5,1) ;
              (2,1,5) (3,1,4) ]
        """
        m = dqi.DqiMatrix.parse(t)
        B = [[20, 5],
             [2, 8],
             [10, 3]]
        L = [[1.4, 0.8],
             [0.5, 1.2]]
        r = m.aggregate_mmult(B, L, left=True)
        self.assertEqual(3, r.rows)
        self.assertEqual(2, r.cols)
        self.assertEqual([4, 1, 3], r[0, 0])
        self.assertEqual([3, 1, 4], r[0, 1])
        self.assertEqual([2, 5, 2], r[1, 0])
        self.assertEqual([1, 5, 1], r[1, 1])
        self.assertEqual([2, 1, 5], r[2, 0])
        self.assertEqual([2, 1, 5], r[2, 1])

    def test_aggregate_mmult_right(self):
        t = """
            [ (4,1,3) (3,1,4) ;
              (2,5,2) (1,5,1) ;
              (2,1,5) (2,1,5) ]
        """
        m = dqi.DqiMatrix.parse(t)
        F = [[0.1, 0.4, 0.9],
             [0.8, 0.3, 0.1]]
        G = [[30.5,  22.],
             [6.8,  11.2],
             [15.5,  11.6]]
        r = m.aggregate_mmult(F, G, left=False)
        self.assertEqual(2, r.rows)
        self.assertEqual(2, r.cols)
        self.assertEqual([2, 2, 4], r[0, 0])
        self.assertEqual([2, 2, 4], r[0, 1])
        self.assertEqual([4, 1, 3], r[1, 0])
        self.assertEqual([3, 2, 4], r[1, 1])

if __name__ == '__main__':
    unittest.main()
