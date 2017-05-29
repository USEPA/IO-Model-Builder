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

if __name__ == '__main__':
    unittest.main()
