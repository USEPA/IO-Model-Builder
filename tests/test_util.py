import tempfile
import unittest
import uuid

import iomb.util as util
import numpy


class TestUtil(unittest.TestCase):

    def test_make_uuid(self):
        expected = str(uuid.uuid3(uuid.NAMESPACE_OID, "flow/a/1/b"))
        actual = util.make_uuid("Flow", None, "a", 1, "B")
        self.assertEqual(expected, actual)

    def test_read_csv_as_data_frame(self):
        text = """
        ,C1,C2,C3
        R1,1,2,3
        R2,4,5,6
        """.strip()
        data = ""
        for line in text.split('\n'):
            data += line.strip() + '\n'
        temp = tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False,
                                           prefix='iomb_tests_')
        temp.write(data)
        temp.close()
        data_frame = util.read_csv_data_frame(temp.name)
        self.assertAlmostEqual(1.0, data_frame['c1']['r1'], 1e-16)
        self.assertTrue(type(data_frame['c1']['r1']) is numpy.float64)
        self.assertAlmostEqual(6.0, data_frame['c3']['r2'], 1e-16)
        self.assertTrue(type(data_frame['c3']['r2']) is numpy.float64)


if __name__ == '__main__':
    unittest.main()
