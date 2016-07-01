import iomb
import os
import unittest


class TestIOModel(unittest.TestCase):
    def setUp(self):
        pref = os.path.dirname(__file__) + '/sample_data/sample_'
        self.model = iomb.make_io_model(pref + 'make.csv', pref + 'use.csv',
                                        scrap_sectors=['Scrap'])

    def test_value_added_sectors(self):
        va = self.model.value_added_sectors
        self.assertEqual(1, len(va))
        self.assertEqual('va', va[0])

    def test_final_demand_sectors(self):
        fd = self.model.final_demand_sectors
        self.assertEqual(1, len(fd))
        self.assertEqual('fd', fd[0])

    def test_industries(self):
        industries = self.model.industries
        self.assertEqual(3, len(industries))
        for i in ['a', 'b', 'c']:
            self.assertTrue(i in industries)

    def test_commodities(self):
        commodities = self.model.commodities
        self.assertEqual(3, len(commodities))
        for i in ['a', 'b', 'c']:
            self.assertTrue(i in commodities)

    def test_get_direct_requirements(self):
        drs = self.model.get_direct_requirements()
        self.assertAlmostEqual(0.152, drs.get_value('a', 'a'), delta=1e-3)
        self.assertAlmostEqual(0.073, drs.get_value('b', 'b'), delta=1e-3)
        self.assertAlmostEqual(0.189, drs.get_value('c', 'c'), delta=1e-3)

    def test_get_market_shares(self):
        ms = self.model.get_market_shares()
        self.assertAlmostEqual(0.909, ms.get_value('a', 'a'), delta=1e-3)
        self.assertAlmostEqual(0.900, ms.get_value('b', 'b'), delta=1e-3)
        self.assertAlmostEqual(0.926, ms.get_value('c', 'c'), delta=1e-3)

    def test_get_non_scrap_ratios(self):
        ratios = self.model.get_non_scrap_ratios()
        col = ratios.columns[0]
        self.assertAlmostEqual(0.991, ratios.get_value('a', col), delta=1e-3)
        self.assertAlmostEqual(0.995, ratios.get_value('b', col), delta=1e-3)
        self.assertAlmostEqual(1.000, ratios.get_value('c', col), delta=1e-3)

    def test_get_transformation_matrix(self):
        tm = self.model.get_transformation_matrix()
        self.assertAlmostEqual(0.917, tm.get_value('a', 'a'), delta=1e-3)
        self.assertAlmostEqual(0.904, tm.get_value('b', 'b'), delta=1e-3)
        self.assertAlmostEqual(0.926, tm.get_value('c', 'c'), delta=1e-3)

    def test_get_dr_coefficients(self):
        drc = self.model.get_dr_coefficients()
        self.assertAlmostEqual(0.166, drc.get_value('a', 'a'), delta=1e-3)
        self.assertAlmostEqual(0.109, drc.get_value('b', 'b'), delta=1e-3)
        self.assertAlmostEqual(0.202, drc.get_value('c', 'c'), delta=1e-3)

    def test_get_tr_coefficients(self):
        trc = self.model.get_tr_coefficients()
        self.assertAlmostEqual(2.487, trc.get_value('a', 'a'), delta=1e-3)
        self.assertAlmostEqual(2.300, trc.get_value('b', 'b'), delta=1e-3)
        self.assertAlmostEqual(2.323, trc.get_value('c', 'c'), delta=1e-3)

if __name__ == '__main__':
    unittest.main()
