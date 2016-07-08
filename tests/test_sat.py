import iomb.sat as sat
import unittest


class TestSat(unittest.TestCase):
    def test_entry_no_optional_fields(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 42.42, 'kg']
        entry = sat.Entry.from_csv(row)
        self.assertIsNone(entry.data_quality)
        self.assertAlmostEqual(42.42, entry.value)

    def test_entry_data_quality(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 42.42, 'kg', '', '', '', '', '', '5', '3', '', 'n.a.', '1',
               '2007']
        entry = sat.Entry.from_csv(row)
        self.assertEqual('(5;3;n.a.;n.a.;1)', entry.data_quality)
        self.assertAlmostEqual(42.42, entry.value)


if __name__ == '__main__':
    unittest.main()
