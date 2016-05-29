import iomb
import unittest


class TestIOModel(unittest.TestCase):
    def setUp(self):
        path = './sample_data/sample_'
        self.model = iomb.make_io_model(path + 'make.csv', path + 'use.csv',
                                        scrap='Scrap')

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

"""

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

    def test_get_dr_coefficients(self):
        drc = self.em.get_dr_coefficients()
        print(drc)  # TODO: test something

    def test_get_tr_coefficients(self):
        trc = self.em.get_tr_coefficients()
        print(trc)  # TODO: test something
"""

if __name__ == '__main__':
    unittest.main()
