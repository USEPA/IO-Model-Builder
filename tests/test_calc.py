import iomb
import iomb.calc as calc
import os
import unittest


class TestCalc(unittest.TestCase):
    def setUp(self):
        pref = os.path.dirname(__file__) + "/sample_data/sample_"
        drc = iomb.read_csv_data_frame(pref + "drc.csv")
        sat = iomb.read_csv_data_frame(pref + "sat.csv")
        demand = {'4/electricity/us': 2, '7/steel parts/us-ga': 2,
                  '9/car manufacture/us-ga': 1}
        self.r = calc.Calculator(drc, sat, demand).calculate()

    def test_totals(self):
        print(self.r.flow_results)

if __name__ == '__main__':
    unittest.main()
