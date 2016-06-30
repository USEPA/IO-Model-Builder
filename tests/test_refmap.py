import iomb.refmap as refmap
import unittest


class TestRefMap(unittest.TestCase):

    def test_compartment_map(self):
        cm = refmap.CompartmentMap.create_default()
        e = cm.get('air/unspecified')
        self.assertEqual(e.compartment, 'air')
        self.assertEqual(e.sub_compartment, 'unspecified')
        self.assertEqual(e.uid, '2d9498c8-6873-45e1-af33-e1a298c119b9')
        self.assertEqual(e.direction, 'output')

    def test_unit_map(self):
        um = refmap.UnitMap.create_default()
        e = um.get('kg')
        self.assertEqual(e.unit, 'kg')
        self.assertEqual(e.unit_uid, '20aadc24-a391-41cf-b340-3e4529f44bde')
        self.assertEqual(e.quantity, 'Mass')
        self.assertEqual(
            e.quantity_uid, '93a60a56-a3c8-11da-a746-0800200b9a66')

    def test_location_map(self):
        lm = refmap.LocationMap.create_default()
        e = lm.get('US-GA')
        self.assertEqual(e.code, 'US-GA')
        self.assertEqual(e.name, 'United States, Georgia')
        self.assertEqual(e.uid, '2b701fc6-ef0e-3b9a-9f4d-631863e904f6')


if __name__ == '__main__':
    unittest.main()
