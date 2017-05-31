import csv
import os
import struct

import iomb
import iomb.dqi as dqi


class Export(object):

    def __init__(self, model):
        self.model = model
        self.folder = 'data'

    def to_dir(self, folder: str):
        """ Exports the matrices of the model to the given folder.

            Args:
                folder (str): the path to the export folder
        """
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        # TODO: currently only supports models with LCIA methods

        # the direct requirements matrix: A
        A = self.model.drc_matrix
        self.__write_matrix(A.values, 'A')

        # the Leontief inverse: L
        L = iomb.calc.leontief_inverse(A)
        self.__write_matrix(L.values, 'L')

        # the satellite matrix: B
        B = self.model.sat_table.as_data_frame().reindex(
            columns=A.index, fill_value=0.0)
        self.__write_matrix(B.values, 'B')

        # the characterization factors: C
        C = self.model.ia_table.as_data_frame().reindex(
            columns=B.index, fill_value=0.0)
        self.__write_matrix(C.values, 'C')

        # the direct impacts per 1 USD sector output: D
        D = C.values @ B.values
        self.__write_matrix(D, 'D')

        # the upstream impacts per 1 USD sector output: U
        U = D @ L.values
        self.__write_matrix(U, 'U')

        # the data quality matrix of the satellite table: B_dqi
        B_dqi = dqi.Matrix.from_sat_table(self.model.sat_table)
        B_dqi.to_csv('%s/B_dqi.csv' % self.folder)

        # the data quality matrix of the direct impacts: D_dqi
        D_dqi = B_dqi.aggregate_mmult(C.values, B.values, left=False)
        D_dqi.to_csv('%s/D_dqi.csv')

        # the data quality matrix of the upstream impacts: U_dqi
        U_dqi = D_dqi.aggregate_mmult(D, L.values, left=True)
        U_dqi.to_csv('%s/U_dqi.csv')

        # write matrix indices with meta-data
        self.__write_sectors(A)
        self.__write_flows(B)
        self.__write_indicators(C)

    def __write_matrix(self, M, name: str):
        path = '%s/%s.bin' % (self.folder, name)
        with open(path, 'wb') as f:
            rows, cols = M.shape
            f.write(struct.pack("<i", rows))
            f.write(struct.pack("<i", cols))
            for col in range(0, cols):
                for row in range(0, rows):
                    val = M[row, col]
                    f.write(struct.pack("<d", val))

    def __write_sectors(self, A):
        path = '%s/sectors.csv' % self.folder
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'ID', 'Name', 'Code', 'Location'])
            i = 0
            for sector_key in A.index:
                sector = self.model.sectors.get(sector_key)
                writer.writerow([i, sector_key, sector.name, sector.code,
                                 sector.location])
                i += 1

    def __write_flows(self, B):
        path = '%s/flows.csv' % self.folder
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'ID', 'Name', 'Category', 'Sub-Category',
                             'Unit', 'UUID'])
            i = 0
            for flow_key in B.index:
                flow = self.model.sat_table.get_flow(flow_key)
                writer.writerow([i, flow.key, flow.name, flow.category,
                                 flow.sub_category, flow.unit, flow.uid])
                i += 1

    def __write_indicators(self, C):
        path = '%s/indicators.csv' % self.folder
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'ID', 'Name', 'Code', 'Unit', 'UUID'])
            i = 0
            for cat_key in C.index:
                idx = self.model.ia_table.category_idx.get(cat_key)
                cat = self.model.ia_table.categories[idx]
                writer.writerow([i, cat_key, cat.name, '',
                                 cat.ref_unit, cat.uid])
                i += 1
