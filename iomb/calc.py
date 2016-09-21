import iomb.model as iom
import logging as log
import numpy as np
import numpy.linalg as linalg
import pandas as pd

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

        # flow contributions to the LCIA results as a data frame with the LCIA
        # categories in the rows, flows in the columns, and flow results times
        # LCIA factors in the cells
        self.lcia_flow_contributions = None


def calculate(model: iom.Model, demand: dict,
              perspective=DIRECT_PERSPECTIVE) -> Result:
    """
    Calculates a result for the given model and demand.

    :param model: The input-output model that should be calculated.
    :param demand: A dictionary containing the demand values of input-output
           sectors
    :param perspective: The perspective of the contribution results. See the
           documentation for more information about the different result
           perspectives. """

    # prepare demand vector, inverse and scaling vector
    drc = model.drc_matrix
    dev = demand_vector(drc, demand)
    inv = leontief_inverse(drc)
    sca = scaling_vector(inv, dev)

    # prepare satellite and LCIA matrix
    sat = model.sat_table.as_data_frame()
    # align columns of satellite matrix with DRC matrix (sector index)
    sat = sat.reindex(columns=drc.columns, fill_value=0.0)
    iaf = None
    if model.ia_table is not None:
        iaf = model.ia_table.as_data_frame()
        # align columns of LCIA factors with satellite matrix rows (flow index)
        iaf = iaf.reindex(columns=sat.index, fill_value=0.0)

    # calculate the total results
    r = Result(perspective)
    r.lci_total = sat.dot(sca)
    if isinstance(r.lci_total, pd.Series):
        r.lci_total = r.lci_total.to_frame('Total')
    if iaf is not None:
        r.lcia_total = iaf.dot(r.lci_total)
        if isinstance(r.lcia_total, pd.Series):
            r.lcia_total = r.lcia_total.to_frame('Total')
        r.lcia_flow_contributions = scale_columns(iaf, r.lci_total.as_matrix())

    # calculate LCI contributions
    if perspective == DIRECT_PERSPECTIVE:
        r.lci_contributions = scale_columns(sat, sca)
    elif perspective == INTERMEDIATE_PERSPECTIVE:
        upstream = sat.dot(inv)
        r.lci_contributions = scale_columns(upstream, sca)
    elif perspective == FINAL_PERSPECTIVE:
        upstream = sat.dot(inv)
        r.lci_contributions = scale_columns(upstream, dev)

    # calculate LCIA contributions
    if iaf is not None and r.lci_contributions is not None:
        r.lcia_contributions = iaf.dot(r.lci_contributions)

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


def get_top(df: pd.DataFrame, row_key=None, column_key=None,
            count=5) -> pd.DataFrame:
    """
    This function takes a data frame and selects the top contributions of the
    given row (selected by the row_key parameter) or column (selected by the
    column_key parameter). It returns a data frame with the top 5 contributors
    (the number of contributors can be modified via the count parameter) and the
    sum of the other elements.
    """
    if row_key is None and column_key is None:
        log.error('either a row_key or a column_key must be specified')
        return
    series = df.loc[row_key, :] if column_key is None else df.loc[:, column_key]
    total = series.sum()
    series = series.sort_values(ascending=False)
    top = len(series) if count > len(series) else count
    series = series.take([i for i in range(0, top)])
    others = total - series.sum()
    series.set_value('Others', others)
    return series.to_frame(row_key if column_key is None else column_key)
