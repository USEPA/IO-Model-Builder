import openio as io
import unittest


class TestEconomicModule(unittest.TestCase):

    def setUp(self):
        self.df = io.DataFolder('./sample_data')
        self.em = self.df.get_economic_module()

    def test_files_present(self):
        self.assertTrue(self.df.has_file(io.USE_TABLE))
        self.assertTrue(self.df.has_file(io.MAKE_TABLE))

if __name__ == '__main__':
    unittest.main()
