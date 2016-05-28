import pandas as pd
import numpy as np
import iomb.util as util


class Result(object):
    """ Contains the results of a calculation. """

    def __init__(self, drc: pd.DataFrame, totals: pd.DataFrame):
        self.drc = drc
        self.totals = totals


class Calculator(object):
    """
    Calculates results from an input-output model for a given demand vector. It
    gets the direct requirements coefficients (drc) and satellite accounts as
    pandas data frames. The demand vector is a simple dictionary that contains
    the sector keys with the respective amounts, e.g.:

    demand = {'1111a0/oilseed farming/us': 1.0}
    """

    def __init__(self, drc: pd.DataFrame, sat: pd.DataFrame, demand: dict):
        self.drc = drc
        self.sat = sat
        self.demand = demand

    def calculate(self) -> Result:
        """ Runs a new calculation and returns a result object. """
        drc = self.drc.copy()
        sat = self.sat.copy().reindex(columns=drc.columns)
        inv = util.leontief(drc)
        demand = self._demand_vector()
        scaling = inv.as_matrix().dot(demand)
        totals = sat.as_matrix().dot(scaling)
        total_result = pd.DataFrame(data=totals, index=sat.index,
                                    columns=['total'])
        return Result(drc, total_result)

    def _demand_vector(self) -> np.ndarray:
        d = np.zeros(self.drc.shape[0])
        index = self.drc.index
        for key, val in self.demand.items():
            loc = index.get_loc(key)
            d[loc] = val
        return d
