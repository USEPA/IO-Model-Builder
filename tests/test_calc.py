import iomb
import iomb.calc as calc
import unittest


class TestCalc(unittest.TestCase):
    def setUp(self):
        drc = iomb.read_csv_data_frame("./sample_data/sample_drc.csv")
        sat = iomb.read_csv_data_frame("./sample_data/sample_sat.csv")
        demand = {'4/electricity/us': 2, '7/steel parts/us-ga': 2,
                  '9/car manufacture/us-ga': 1}
        self.r = calc.Calculator(drc, sat, demand).calculate()

    def test_totals(self):
        print(self.r.flow_results)

if __name__ == '__main__':
    unittest.main()