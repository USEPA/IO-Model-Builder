import pandas as pd
import numpy as np
import iomb.util as util


class Result(object):
    """ Contains the results of a calculation. """

    def __init__(self):
        self.flows = None
        self.sectors = None
        self.demand = None
        self.scaling = None
        self.totals_lci = None

    @property
    def demand_vector(self) -> pd.DataFrame:
        return pd.DataFrame(data=self.demand, index=self.sectors,
                            columns=['final demand'])

    @property
    def scaling_vector(self):
        return pd.DataFrame(data=self.scaling, index=self.sectors,
                            columns=['scaling factor'])

    @property
    def flow_results(self):
        return pd.DataFrame(data=self.totals_lci, index=self.flows,
                            columns=['total result'])


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

        # prepare the result
        r = Result()
        drc = self.drc.copy()
        sat = self.sat.copy().reindex(columns=drc.columns, fill_value=0.0)
        r.sectors = drc.index
        r.flows = sat.index
        r.demand = self._demand_vector()

        inv = util.leontief(drc)
        r.scaling = inv.as_matrix().dot(r.demand)
        r.totals_lci = sat.as_matrix().dot(r.scaling)
        return r

    def _demand_vector(self) -> np.ndarray:
        d = np.zeros(self.drc.shape[0])
        index = self.drc.index
        for key, val in self.demand.items():
            loc = index.get_loc(key)
            d[loc] = val
        return d
