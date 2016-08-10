import iomb
import iomb.calc as calc
import os
import tempfile as tempf
import unittest
import iomb.validation as validation

_DRC = """        , 1/electricity/us , 2/steel parts/us , 3/car assembly/us
1/electricity/us  , 0.1              , 0.3              , 0.1
2/steel parts/us  , 0                , 0.1              , 0.2
3/car assembly/us , 0                , 0                , 0.1
"""

_SAT = """ Flow , CAS , Category , SubCategory , UUID , Process     , Code , Location , Amount , Unit
Water           ,     , resource , in water    ,      , electricity , 1    , US       , 5      , kg
Carbon dioxide  ,     , air      , unspecified ,      , electricity , 1    , US       , 3      , kg
Sulfur dioxide  ,     , air      , unspecified ,      , electricity , 1    , US       , 0.2    , kg
Water           ,     , resource , in water    ,      , steel parts , 2    , US       , 2      , kg
Carbon dioxide  ,     , air      , unspecified ,      , steel parts , 2    , US       , 2      , kg
Sulfur dioxide  ,     , air      , unspecified ,      , steel parts , 2    , US       , 0.1    , kg
"""

_SECTORS = """ Code , Name         , Category , SubCategory , Location
               1    , electricity  ,          ,             , US
               2    , steel parts  ,          ,             , US
               3    , car assembly ,          ,             , US
"""

_LCIA = """ Method  , LCIA-Category            , Ref.Unit , Flow           , Compartment , Sub-Compartment , Unit , Flow-UUID , Amount
SimpleEconomyMethod , Carbon dioxide emissions , kgCO2e   , Carbon dioxide , air         , unspecified     , kg   ,           , 1
SimpleEconomyMethod , Sulfur dioxide emissions , kgSO2e   , Sulfur dioxide , air         , unspecified     , kg   ,           , 1
SimpleEconomyMethod , Water use                , kgH2Oe   , Water          , resource    , in water        , kg   ,           , 1
"""


def tf(text: str) -> str:
    """ Creates a temporary file with the given text data and returns the name
        of this file. """
    temp = tempf.NamedTemporaryFile('w', encoding='utf-8', delete=False,
                                    prefix='iomb_tests_')
    temp.write(text)
    temp.close()
    return temp.name


class TestCalc(unittest.TestCase):
    def setUp(self):
        drc = tf(_DRC)
        sat = tf(_SAT)
        sectors = tf(_SECTORS)
        lcia = tf(_LCIA)
        self.paths = [drc, sat, sectors, lcia]
        self.model = iomb.make_model(drc, [sat], sectors, [lcia])
        self.demand = {'3/car assembly/us': 1}

    def tearDown(self):
        for path in self.paths:
            os.remove(path)

    def test_is_valid(self):
        vr = validation.validate(self.model)
        self.assertFalse(vr.failed)

    def test_direct_perspective(self):
        r = calc.calculate(self.model, self.demand, calc.DIRECT_PERSPECTIVE)
        print(r.lci_total)
        print(r.lcia_total)

if __name__ == '__main__':
    unittest.main()
