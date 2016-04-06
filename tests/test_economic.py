import openio as io
import unittest


class TestEconomicModule(unittest.TestCase):

    def test_files_present(self):
        folder = io.DataFolder('../data')
        self.assertTrue(folder.has_file(io.USE_TABLE))
        self.assertTrue(folder.has_file(io.MAKE_TABLE))

if __name__ == '__main__':
    unittest.main()
