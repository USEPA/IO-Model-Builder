"""
This script converts the BEA make and use Excel tables into CSV files that can
be used in the OpenIO model builder.

Download the Excel files (Make and Use tables, after redefinitions, producer value)
from http://www.bea.gov/industry/io_annual.htm

!!! Before running this script delete the intermediate sum row and column from the
    use table !!!

"""

import csv
import xlrd


class Config(object):

    def __init__(self, rows_end=0, cols_end=0):
        self.rows_start = 6
        self.rows_end = rows_end
        self.cols_start = 2
        self.cols_end = cols_end


def main():
    convert_use_table()
    convert_make_table()


def convert_use_table():
    wb_path = 'IOUse_After_Redefinitions_PRO_2007_Detail.xlsx'
    wb = xlrd.open_workbook(wb_path)
    sheet = wb.sheet_by_name('2007')
    conf = Config(rows_end=398, cols_end=411)
    with open('use_table_2007.csv', 'w', newline='\n', encoding="utf8") as f:
        writer = csv.writer(f)
        write_columns(sheet, writer, conf)
        write_rows(sheet, writer, conf)


def convert_make_table():
    wb_path = 'IOMake_After_Redefinitions_2007_Detail.xlsx'
    wb = xlrd.open_workbook(wb_path)
    sheet = wb.sheet_by_name('2007')
    conf = Config(rows_end=395, cols_end=394)
    with open('make_table_2007.csv', 'w', newline='\n', encoding="utf8") as f:
        writer = csv.writer(f)
        write_columns(sheet, writer, conf)
        write_rows(sheet, writer, conf)


def write_columns(sheet, writer, conf):
    labels = [""]
    for col in range(conf.cols_start, conf.cols_end):
        code = get_code(sheet.cell(5, col).value)
        name = sheet.cell(4, col).value.strip()
        col_label = "%s - %s" % (code, name)
        labels.append(col_label)
    writer.writerow(labels)


def write_rows(sheet, writer, conf):
    for row in range(conf.rows_start, conf.rows_end):
        values = []
        r_code = get_code(sheet.cell(row, 0).value)
        r_name = sheet.cell(row, 1).value.strip()
        row_label = '%s - %s' % (r_code, r_name)
        values.append(row_label)
        for col in range(conf.cols_start, conf.cols_end):
            val = sheet.cell(row, col).value
            if type(val) in (float, int):
                values.append(val)
            else:
                values.append(0.0)
        writer.writerow(values)


def get_code(cell_value: object) -> str:
    if type(cell_value) == float:
        return str(int(cell_value))
    elif type(cell_value) == str:
        return cell_value.strip()
    else:
        return ''


if __name__ == '__main__':
    main()
