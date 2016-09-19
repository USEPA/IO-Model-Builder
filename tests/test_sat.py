import iomb.sat as sat
import unittest


class TestSat(unittest.TestCase):
    def test_entry_no_optional_fields(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 42.42, 'kg']
        entry = sat.Entry.from_csv(row)
        self.assertIsNone(entry.data_quality_entry)
        self.assertAlmostEqual(42.42, entry.value)

    def test_entry_data_quality(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 42.42, 'kg', '', '', '', '', '', '5', '3', '', 'n.a.', '1',
               '2007']
        entry = sat.Entry.from_csv(row)
        self.assertEqual('(5;3;n.a.;n.a.;1)', entry.data_quality_entry)
        self.assertAlmostEqual(42.42, entry.value)

    def test_add_data_quality(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 1, 'kg', '', '', '', '', '', '1', '2', '3', '4', '5',
               '2007']
        entry = sat.Entry.from_csv(row)
        self.assertEqual('(1;2;3;4;5)', entry.data_quality_entry)
        entry.add(2, data_quality_entry='(5;4;3;2;1)')
        self.assertEqual('(4;3;3;3;2)', entry.data_quality_entry)

if __name__ == '__main__':
    unittest.main()
