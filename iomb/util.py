import csv
import uuid


def make_uuid(*args: list) -> str:
    path = as_path(*args)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))


def as_path(*args: list) -> str:
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).lower())
    return "/".join(strings)


def uuid_of_process(sector_name: str, sector_code: str, location: str) -> str:
    return make_uuid('Process', sector_name, sector_code, location)


def uuid_of_product(sector_name: str, sector_code: str, location: str) -> str:
    return make_uuid('Flow', sector_name, sector_code, location)


def uuid_of_flow(name: str, category: str, sub_category: str, unit: str) -> str:
    return make_uuid('Flow', name, category, sub_category, unit)


def each_csv_row(csv_file, func, skip_header=False):
    """ Iterates over each row in the given CSV file. It skips the first row if
        specified and removes leading and trailing whitespaces.
    """
    with open(csv_file) as f:
        reader = csv.reader(f)
        i = 0
        if skip_header:
            next(reader)
            i += 1
        for row in reader:
            r = [v.strip() for v in row]
            func(r, i)
            i += 1
