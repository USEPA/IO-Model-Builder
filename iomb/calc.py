import pandas as pd
import numpy as np
import numpy.linalg as linalg
import logging as log


class Result(object):
    """ Contains the results of a calculation. """

    def __init__(self):
        # inventory result
        self.direct_contributions = None
        self.total_result = None

        # impact assessment result
        self.direct_ia_contributions = None
        self.total_ia_result = None


def calculate(demand: dict, drc: pd.DataFrame, sat: pd.DataFrame, iaf=None) -> Result:
    """
    Calculates a result for the given demand.

    :param demand: A dictionary containing the demand values of input-output sectors
    :param drc: A data frame (sector x sector) with the direct requirements coefficients.
    :param sat: A data frame (flow x sector) with the satellite table data.
    :param iaf: An optional data frame (ia-category x flow) with characterization factors
                for impact assessment.
    """
    dev = demand_vector(drc, demand)
    inv = leontief_inverse(drc)
    sca = scaling_vector(inv, dev)
    del inv  # later we may also want to calculate upstream totals

    r = Result()
    # flow results
    sat_ = sat.reindex(columns=drc.columns, fill_value=0.0)  # align columns with DRC matrix
    r.direct_contributions = scale_columns(sat_, sca)
    del sat_
    r.total_result = column_totals(r.direct_contributions)

    # impact assessment result
    if iaf is not None:
        iaf_ = iaf.reindex(columns=sat.index, fill_value=0.0)  # align columns with SAT matrix rows
        r.direct_ia_contributions = iaf_.dot(r.direct_contributions)
        del iaf_
        r.total_ia_result = column_totals(r.direct_ia_contributions)

    return r

def leontief_inverse(a: pd.DataFrame) -> pd.DataFrame:
    """ Calculates the Leontief-inverse (I-A)^-1 for the given matrix A. """
    eye = np.eye(a.shape[0], dtype=np.float64)
    inv = linalg.inv(eye - a.values)
    return pd.DataFrame(inv, index=a.index, columns=a.columns)


def demand_vector(a: pd.DataFrame, demand: dict) -> np.ndarray:
    """ Creates numeric vector from the demand map and the matrix A. """
    v = np.zeros(a.shape[0], dtype=np.float64)
    idx = a.index
    for key, val in demand.items():
        if val == 0:
            continue
        k = key.lower()
        if k not in idx:
            log.error('demand %s is not contained in A', k)
            continue
        i = idx.get_loc(k)
        v[i] = val
    return v


def scaling_vector(inv: pd.DataFrame, dev: np.ndarray) -> np.ndarray:
    """ Calculates the scaling vector from the given leontief inverse
        and demand vector. """
    s = np.zeros(dev.shape[0], dtype=np.float64)
    inv_data = inv.values
    for i in range(0, dev.shape[0]):
        d = dev[i]
        if d == 0:
            continue
        col = inv_data[:, i]
        s += d * col
    return s


def scale_columns(m: pd.DataFrame, v: np.ndarray) -> pd.DataFrame:
    """ Creates a new data frame from the given matrix M where
        each column is scaled with the value of the given vector v:
        M * diag(v) """
    values = m.values
    result = np.zeros(values.shape, dtype=np.float64)
    for i in range(0, v.shape[0]):
        s = v[i]
        if s == 0:
            continue
        result[:, i] = s * values[:, i]
    return pd.DataFrame(result, index=m.index, columns=m.columns)


def column_totals(m: pd.DataFrame) -> pd.DataFrame:
    """ Calculates the column totals of the given data frame. """
    totals = np.sum(m.values, axis=1, dtype=np.float64)
    return pd.DataFrame(totals, index=m.index, columns=['total'])
