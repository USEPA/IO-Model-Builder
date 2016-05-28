import iomb.model as model
import unittest


class TestModel(unittest.TestCase):
    def test_flow_key(self):
        flow = model.ElemFlow(name='Carbon dioxide', category='air',
                              sub_category='unspecified', unit='kg')
        expected = 'air/unspecified/carbon dioxide/kg'
        self.assertEqual(expected, flow.key)

    def test_sector_key(self):
        sector = model.Sector(code='1111A0', name='Oilseed farming',
                              location='US')
        expected = '1111a0/oilseed farming/us'
        self.assertEqual(expected, sector.key)

if __name__ == '__main__':
    unittest.main()
