"""
Writes model demands to a json and an overview csv file for use with the USEEIO API.
See doc/data format#Demand vectors for the data format specification for demand.
"""
import csv
import json
import os

##Configure script. Enter csv file for demand and a path to the file
CSV_FILE = '../example/demand.csv'
MODEL_PATH = '../example/matrices'

COL_CODE = 0
COL_NAME = 1
COL_LOCATION = 2
COL_FIRST_DEMAND = 3


class DemandInfo(object):

    def __init__(self, column_header: str):
        parts = column_header.split('_')
        self.year = int(parts[0])
        self.location = parts[1]
        self.perspective = parts[2]
        self.system = parts[3] if len(parts) > 3 else 'Full System'
        self.id = column_header.lower()

    def to_csv_row(self):
        return [self.id, self.year, self.perspective, self.system,
                self.location]


def main():
    prepare_folders()
    rows = read_csv_rows()
    infos = []
    for col in range(COL_FIRST_DEMAND, len(rows[0])):
        header = rows[0][col]
        info = DemandInfo(header)
        infos.append(info.to_csv_row())
        entries = read_demand_entries(rows, col)
        dump_json(entries, os.path.join(
            MODEL_PATH, 'demands', info.id + '.json'))
    write_infos(infos)


def prepare_folders():
    folder = os.path.join(MODEL_PATH, 'demands')
    if not os.path.exists(folder):
        os.makedirs(folder)


def write_infos(infos):
    path = os.path.join(MODEL_PATH, 'demands.csv')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Year', 'Type', 'System', 'Location'])
        for row in infos:
            writer.writerow(row)


def read_csv_rows():
    rows = []
    with open(CSV_FILE, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def read_demand_entries(rows, col_idx):
    entries = []
    for row_idx in range(1, len(rows)):
        amount = float(rows[row_idx][col_idx])
        if amount == 0.0:
            continue
        sector_id = get_sector_id(row_idx, rows)
        entries.append({'sector': sector_id, 'amount': amount})
    return entries


def get_sector_id(row_idx: int, rows: list) -> str:
    row = rows[row_idx]
    parts = [row[COL_CODE], row[COL_NAME], row[COL_LOCATION]]
    sector_id = '/'.join(x.strip().lower() for x in parts)
    return sector_id


def dump_json(obj, file_name: str):
    with open(file_name, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, indent='  ')


if __name__ == '__main__':
    main()
