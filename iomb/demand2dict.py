import csv
import iomb.refmap as ref


def demandtodict(vector_name, csv_file):
    demand = {}
    with open(csv_file, 'r', encoding='utf8', newline='\n') as f:
        reader = csv.reader(f)

        # find the vector index
        header = next(reader)
        idx = -1
        for i in range(3, len(header)):
            if header[i] == vector_name:
                idx = i
                break
        if idx == -1:
            print('%s not found' % vector_name)
            return

        print('take values for %s from colum %s' % (vector_name, idx + 1))

        for row in reader:

            value = float(row[idx])
            if value == 0:
                continue

            sector = ref.Sector()
            sector.code = row[0]
            sector.name = row[1]
            sector.location = row[2]
            demand[sector.key] = value

    return demand
