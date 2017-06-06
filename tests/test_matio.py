import os
import tempfile
import unittest

import iomb.matio as matio
import numpy


class TestMatio(unittest.TestCase):

    def test_matio(self):
        M = numpy.array([[1, 2, 3], [4, 5, 6]], dtype=numpy.float)
        self.assertEqual((2, 3), M.shape)
        tf = tempfile.NamedTemporaryFile(delete=False)
        matio.write_matrix(M, tf.name)
        self.assertEqual((2, 3), matio.read_shape(tf.name))
        N = matio.read_matrix(tf.name)
        self.assertEqual(M.shape, N.shape)
        for row in range(0, M.shape[0]):
            for col in range(0, M.shape[1]):
                self.assertAlmostEqual(M[row, col], N[row, col], places=16)
        try:
            del N
            tf.close()
            os.remove(tf.name)
        except:
            print('failed to delete temp-file: ' + tf.name)
            pass

if __name__ == '__main__':
    unittest.main()
