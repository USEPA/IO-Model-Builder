import csv
import uuid
import logging as log

import numpy
import pandas as pd


def make_uuid(*args: str) -> str:
    path = as_path(*args)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))


def as_path(*args: str) -> str:
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).strip().lower())
    return "/".join(strings)


def is_empty_str(s: str) -> bool:
    if s is None:
        return True
    if isinstance(s, str):
        return s.strip() == ''
    else:
        log.error('expected string but got %s', s)
        return False


def each_csv_row(csv_file: str, func, skip_header=False, encoding='utf-8'):
    """ Iterates over each row in the given CSV file. It skips the first row if
        specified and removes leading and trailing whitespaces.
    """
    log.info('parse CSV file %s', csv_file)
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


def read_csv_data_frame(csv_file, keys_to_lower=True) -> pd.DataFrame:
    """ Loads a pandas DataFrame from the given CSV file. """
    log.info('read data frame from %s', csv_file)
    df = pd.read_csv(csv_file, index_col=0, header=0)
    df.fillna(0.0, inplace=True)

    def strip(x: str):
        r = x.strip()
        if keys_to_lower:
            r = r.lower()
        return r

    df.rename(index=strip, columns=strip, inplace=True)
    return df


def csv_val(row: list, idx: int, default=None):
    if idx >= len(row):
        return default
    else:
        return row[idx]
