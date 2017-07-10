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
        other = sat.Entry(2.0)
        other.data_quality_entry = '(5;4;3;2;1)'
        entry.add(other)
        self.assertEqual('(4;3;3;3;2)', entry.data_quality_entry)

    def test_no_comment(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 1, 'kg', '', '', '', '', '', '1', '2', '3', '4', '5',
               '', None, '', None]
        entry = sat.Entry.from_csv(row)
        self.assertIsNone(entry.comment)

    def test_comment(self):
        row = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
               'US', 1, 'kg', '', '', '', '', '', '1', '2', '3', '4', '5',
               '2013', 'CO2', 'USEPA, 2016a', 'Other']
        entry = sat.Entry.from_csv(row)
        self.assertEqual('2013', entry.year)
        self.assertEqual('CO2', entry.tags)
        self.assertEqual('USEPA, 2016a', entry.sources)
        self.assertEqual('Other', entry.comment)

    def test_add_comment(self):
        row1 = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
                'US', 1, 'kg', '', '', '', '', '', '1', '2', '3', '4', '5',
                '2013', 'CO2', 'USEPA, 2016a', 'Other']
        e1 = sat.Entry.from_csv(row1)
        row2 = ['CO2', '', 'air', 'unspecified', '123', 'agriculture', 'abc',
                'US', 1, 'kg', '', '', '', '', '', '1', '2', '3', '4', '5',
                '2017', 'CH4', 'USEPA, 2016a', 'More other']
        e2 = sat.Entry.from_csv(row2)
        e1.add(e2)
        self.assertEqual('2013; 2017', e1.year)
        self.assertEqual('CO2; CH4', e1.tags)
        self.assertEqual('USEPA, 2016a', e1.sources)
        self.assertEqual('Other; More other', e1.comment)

if __name__ == '__main__':
    unittest.main()
