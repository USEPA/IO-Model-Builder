import iomb.refmap as refmap
import unittest


class TestRefMap(unittest.TestCase):

    def test_unit_map(self):
        um = refmap.UnitMap.create_default()
        e = um.get('kg')
        self.assertEqual(e.unit_name, 'kg')
        self.assertEqual(e.unit_uid, '20aadc24-a391-41cf-b340-3e4529f44bde')
        self.assertEqual(e.quantity_name, 'Mass')
        self.assertEqual(
            e.quantity_uid, '93a60a56-a3c8-11da-a746-0800200b9a66')

if __name__ == '__main__':
    unittest.main()
