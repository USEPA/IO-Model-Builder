import openio as io
import unittest


class TestEconomicModule(unittest.TestCase):

    def setUp(self):
        self.df = io.DataFolder('./sample_data')
        self.em = self.df.get_economic_module()

    def test_files_present(self):
        self.assertTrue(self.df.has_file(io.USE_TABLE))
        self.assertTrue(self.df.has_file(io.MAKE_TABLE))

    def test_get_industries(self):
        industries = self.em.get_industries()
        self.assertEqual(3, len(industries))
        for ind in ['A', 'B', 'C']:
            self.assertTrue(ind in industries)

    def test_get_commodities(self):
        commodities = self.em.get_commodities()
        self.assertEqual(4, len(commodities))
        for com in ['A', 'B', 'C', 'Scrap']:
            self.assertTrue(com in commodities)

if __name__ == '__main__':
    unittest.main()
