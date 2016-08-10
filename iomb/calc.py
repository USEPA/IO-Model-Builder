import pandas as pd
import numpy as np
import numpy.linalg as linalg
import logging as log

DIRECT_PERSPECTIVE = 'direct'
INTERMEDIATE_PERSPECTIVE = 'intermediate'
FINAL_PERSPECTIVE = 'final'


class Result(object):
    """ Contains the results of a calculation. The impact assessment results
        are 'None' if the calculated model did not contain characterization
        factors. """

    def __init__(self, perspective: str):
        self.perspective = perspective

        # total LCI and LCIA results are equal for all perspectives
        self.lci_total = None
        self.lcia_total = None

        # sector contributions for the selected perspective
        self.lci_contributions = None
        self.lcia_contributions = None


def calculate(demand: dict, drc: pd.DataFrame, sat: pd.DataFrame, iaf=None,
              perspective=DIRECT_PERSPECTIVE) -> Result:
    """
    Calculates a result for the given demand.

    :param demand: A dictionary containing the demand values of input-output
           sectors
    :param drc: A data frame (sector x sector) with the direct requirements
           coefficients.
    :param sat: A data frame (flow x sector) with the satellite table data.
    :param iaf: An optional data frame (ia-category x flow) with
           characterization factors for impact assessment.
    :param perspective: The perspective of the contribution results. See the
           documentation for more information about the different result
           perspectives. """

    # prepare demand vector, inverse and scaling vector
    dev = demand_vector(drc, demand)
    inv = leontief_inverse(drc)
    sca = scaling_vector(inv, dev)

    r = Result(perspective)

    # align columns of satellite matrix with DRC matrix (sector index)
    sat_ = sat.reindex(columns=drc.columns, fill_value=0.0)
    # align columns of LCIA factors with satellite matrix rows (flow index)
    iaf_ = None if iaf is None else iaf.reindex(columns=sat.index,
                                                fill_value=0.0)

    # calculate the total results
    r.lci_total = sat_.dot(sca)
    if iaf_ is not None:
        r.lcia_total = iaf_.dot(r.lci_total)

    # calculate LCI contributions
    if perspective == DIRECT_PERSPECTIVE:
        r.lci_contributions = scale_columns(sat_, sca)
    elif perspective == INTERMEDIATE_PERSPECTIVE:
        upstream = sat_.dot(inv)
        r.lci_contributions = scale_columns(upstream, sca)
    elif perspective == FINAL_PERSPECTIVE:
        upstream = sat_.dot(inv)
        r.lci_contributions = scale_columns(upstream, dev)

    # calculate LCIA contributions
    if iaf_ is not None and r.lci_contributions is not None:
        r.lcia_contributions = iaf_.dot(r.lci_contributions)

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
