import iomb.refmap as ref
import unittest


class TestModel(unittest.TestCase):
    def test_flow_key(self):
        f = ref.ElemFlow()
        f.name = 'Carbon dioxide'
        f.category = 'air'
        f.sub_category = 'unspecified'
        f.unit = 'kg'
        expected = 'air/unspecified/carbon dioxide/kg'
        self.assertEqual(expected, f.key)

    def test_sector_key(self):
        s = ref.Sector()
        s.code = '1111A0'
        s.name = 'Oilseed farming'
        s.location = 'US'
        expected = '1111a0/oilseed farming/us'
        self.assertEqual(expected, s.key)


if __name__ == '__main__':
    unittest.main()
