import csv
import uuid


def make_uuid(*args: list) -> str:
    strings = []
    for arg in args:
        if arg is None:
            continue
        strings.append(str(arg).lower())
    path = "/".join(strings)
    return str(uuid.uuid3(uuid.NAMESPACE_OID, path))


def uuid_of_process(sector_name: str, sector_code: str) -> str:
    return make_uuid('Process', sector_name, sector_code)


def uuid_of_product(sector_name: str, sector_code: str) -> str:
    return make_uuid('Flow', sector_name, sector_code)


def uuid_of_flow(name: str, category: str, sub_category: str) -> str:
    return make_uuid('Flow', name, category, sub_category)


def each_csv_row(csv_file, func):
    """ Iterates over each row in the given CSV file. It skips the first row and
        removes leading and trailing whitespaces.
    """
    with open(csv_file) as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            r = [i.strip() for i in row]
            func(r)
