import iomb
import iomb.model as model
import pandas as pd
import iomb.validation as validation
import tempfile as tempf
import unittest
import os


_DRC = """        , 1/electricity/us , 2/steel parts/us , 3/car assembly/us
1/electricity/us  , 0.1              , 0.3              , 0.1
2/steel parts/us  , 0                , 0.1              , 0.2
3/car assembly/us , 0                , 0                , 0.1
"""

_SAT = """ FlowName,CAS,FlowCategory,FlowSubCategory,FlowUUID,ProcessName,ProcessCode,ProcessLocation,FlowAmount,FlowUnit
Water          ,,resource,in water,,electricity,,,5,kg,,,,,,,,,,,,,,
Carbon dioxide ,,air,unspecified,,electricity,,,3,kg,,,,,,,,,,,,,,
Sulfur dioxide ,,air,unspecified,,electricity,,,0.2,kg,,,,,,,,,,,,,,
Water          ,,resource,in water,,steelparts,,,2,kg,,,,,,,,,,,,,,
Carbon dioxide ,,air,unspecified,,steelparts,,,2,kg,,,,,,,,,,,,,,
Sulfur dioxide ,,air,unspecified,,steelparts,,,0.1,kg,,,,,,,,,,,,,,


"""


def tf(text: str) -> str:
    """ Creates a temporary file with the given text data and returns the name
        of this file. """
    temp = tempf.NamedTemporaryFile('w', encoding='utf-8', delete=False,
                                    prefix='iomb_tests_')
    temp.write(text)
    temp.close()
    return temp.name


class TestValidation(unittest.TestCase):

    def setUp(self):
        self.drc = tf(_DRC)

    def tearDown(self):
        os.remove(self.drc)

    def test_not_a_model(self):
        v = validation.validate('not a model')
        self.assertTrue(v.failed)

    def test_missing_fields(self):
        m = model.Model(None, None, None, None, None, None, None)
        self.assertTrue(validation.validate(m).failed)

if __name__ == '__main__':
    unittest.main()
