import iomb
import unittest


class TestIOModel(unittest.TestCase):
    def setUp(self):
        path = './sample_data/sample_'
        self.model = iomb.make_io_model(path + 'make.csv', path + 'use.csv',
                                        scrap_sector='Scrap')

    def test_value_added_sectors(self):
        va = self.model.value_added_sectors
        self.assertEqual(1, len(va))
        self.assertEqual('VA', va[0])

    def test_final_demand_sectors(self):
        fd = self.model.final_demand_sectors
        self.assertEqual(1, len(fd))
        self.assertEqual('FD', fd[0])

    def test_industries(self):
        industries = self.model.industries
        self.assertEqual(3, len(industries))
        for i in ['A', 'B', 'C']:
            self.assertTrue(i in industries)

    def test_commodities(self):
        commodities = self.model.commodities
        self.assertEqual(3, len(commodities))
        for i in ['A', 'B', 'C']:
            self.assertTrue(i in commodities)

    def test_get_direct_requirements(self):
        drs = self.model.get_direct_requirements()
        self.assertAlmostEqual(0.152, drs.get_value('A', 'A'), delta=1e-3)
        self.assertAlmostEqual(0.073, drs.get_value('B', 'B'), delta=1e-3)
        self.assertAlmostEqual(0.189, drs.get_value('C', 'C'), delta=1e-3)

    def test_get_market_shares(self):
        ms = self.model.get_market_shares()
        self.assertAlmostEqual(0.909, ms.get_value('A', 'A'), delta=1e-3)
        self.assertAlmostEqual(0.900, ms.get_value('B', 'B'), delta=1e-3)
        self.assertAlmostEqual(0.926, ms.get_value('C', 'C'), delta=1e-3)

    def test_get_non_scrap_ratios(self):
        ratios = self.model.get_non_scrap_ratios()
        col = ratios.columns[0]
        self.assertAlmostEqual(0.991, ratios.get_value('A', col), delta=1e-3)
        self.assertAlmostEqual(0.995, ratios.get_value('B', col), delta=1e-3)
        self.assertAlmostEqual(1.000, ratios.get_value('C', col), delta=1e-3)
"""



    def test_get_dr_coefficients(self):
        drc = self.em.get_dr_coefficients()
        print(drc)  # TODO: test something

    def test_get_tr_coefficients(self):
        trc = self.em.get_tr_coefficients()
        print(trc)  # TODO: test something
"""

if __name__ == '__main__':
    unittest.main()
