import csv
import numpy.linalg as linalg
import numpy as np
import pandas as pd
import uuid


def make_uuid(*args: list) -> str:
    path = as_path(*args)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))


def as_path(*args: list) -> str:
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).strip().lower())
    return "/".join(strings)


def uuid_of_flow(name: str, category: str, sub_category: str, unit: str) -> str:
    return make_uuid('Flow', name, category, sub_category, unit)


def each_csv_row(csv_file: str, func, skip_header=False, encoding='utf-8'):
    """ Iterates over each row in the given CSV file. It skips the first row if
        specified and removes leading and trailing whitespaces.
    """
    with open(csv_file, 'r', encoding=encoding, newline='\n') as f:
        reader = csv.reader(f)
        i = 0
        if skip_header:
            next(reader)
            i += 1
        for row in reader:
            r = [v.strip() for v in row]
            func(r, i)
            i += 1


def leontief(a: pd.DataFrame) -> pd.DataFrame:
    """ Calculates the Leontief inverse of the matrix in the given data frame
        and returns a new data frame with the same indices.
    """
    eye = np.eye(a.shape[0], dtype=np.float64)
    data = linalg.inv(eye - a.as_matrix())
    return pd.DataFrame(data=data, index=a.index, columns=a.columns)
