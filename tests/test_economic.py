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

    def test_get_market_shares(self):
        shares = self.em.get_market_shares()
        # print(shares)
        self.assertAlmostEqual(0.909090909, shares['A']['A'], delta=1e-8)
        self.assertAlmostEqual(0.0625, shares['B']['A'], delta=1e-8)
        self.assertAlmostEqual(0.074074074, shares['C']['B'], delta=1e-8)

    def test_get_direct_requirements(self):
        drs = self.em.get_direct_requirements()
        # print(drs)
        self.assertAlmostEqual(50/328, drs['A']['A'], delta=1e-8)
        self.assertAlmostEqual(150/412, drs['B']['C'], delta=1e-8)
        self.assertAlmostEqual(1/265, drs['C']['Scrap'], delta=1e-8)

if __name__ == '__main__':
    unittest.main()
