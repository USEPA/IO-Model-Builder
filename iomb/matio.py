import csv
import os
import struct

import iomb
import iomb.dqi as dqi
import numpy
import logging as log

class Matrices(object):
    """A collection of model matrices"""
    def __init__(self, model, DQImatrices = False):
        # the direct requirements matrix: A
        self.model = model
        self.A = model.drc_matrix
        # the Leontief inverse: L
        self.L = iomb.calc.leontief_inverse(self.A)
        # the satellite matrix: B
        self.B = model.sat_table.as_data_frame().reindex(
            columns=self.A.index, fill_value=0.0)
        # the characterization factors: C
        self.C = model.ia_table.as_data_frame().reindex(
            columns=self.B.index, fill_value=0.0)
        # the direct impacts per 1 USD sector output: D
        self.D = self.C.dot(self.B)
        # the upstream impacts per 1 USD sector output: U
        self.U = self.D.dot(self.L)
        self.component_matrices = {'A':self.A,
                                   'B':self.B,
                                   'C': self.C,
                                   'L': self.L}
        self.result_matrices= {'D':self.D,
                               'U':self.U}

        self.dqi_matrices = {}
        if DQImatrices:
            # the data quality matrix of the satellite table: B_dqi
            self.B_dqi = dqi.Matrix.from_sat_table(model)
            self.dqi_matrices['B_dqi'] = self.B_dqi
            # the data quality matrix of the direct impacts: D_dqi
            try:
                self.D_dqi = self.B_dqi.aggregate_mmult(self.C.values, self.B.values, left=False)
                self.dqi_matrices['D_dqi'] = self.D_dqi
            except KeyError:
                log.warning('D_dqi could not be computed.')
            # the data quality matrix of the upstream impacts: U_dqi
            try:
                self.U_dqi = self.D_dqi.aggregate_mmult(self.D, self.L.values, left=True)
                self.dqi_matrices['U_dqi'] = self.U_dqi
            except KeyError:
                log.warning('U_dqi could not be computed.')

class Export(object):

    def __init__(self, matrices):
        self.folder = 'data'
        self.matrices = matrices
        self.model = matrices.model

    def to_dir(self, folder: str, exportDQImatrices=False):
        """ Exports the matrices of the model to the given folder.

            Args:
                folder (str): the path to the export folder
        """
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        for k, v in self.matrices.component_matrices.items():
            self.__write_matrix(v.values, k)

        for k, v in self.matrices.result_matrices.items():
            self.__write_matrix(v.values, k)

        if exportDQImatrices:
            for k, v in self.matrices.dqi_matrices.items():
                v.to_csv(folder+k+'.csv')

        # write matrix indices with meta-data
        self.__write_sectors(self.matrices.A)
        self.__write_flows(self.matrices.B)
        self.__write_indicators(self.matrices.C)

    def __write_matrix(self, M, name: str):
        path = '%s/%s.bin' % (self.folder, name)
        write_matrix(M, path)

    def __write_sectors(self, A):
        path = '%s/sectors.csv' % self.folder
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow(['Index', 'ID', 'Name', 'Code', 'Location', 'Description'])
            i = 0
            for sector_key in A.index:
                sector = self.model.sectors.get(sector_key)
                writer.writerow([i, sector_key, sector.name, sector.code,
                                 sector.location, sector.description])
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
            writer.writerow(['Index', 'ID', 'Name', 'Code', 'Unit', 'Group'])
            i = 0
            for cat_key in C.index:
                idx = self.model.ia_table.category_idx.get(cat_key)
                cat = self.model.ia_table.categories[idx]
                writer.writerow([i, cat_key, cat.name, cat.code,
                                 cat.ref_unit, cat.group])
            i += 1


def read_shape(file_path: str):
    """ Reads and returns the shape (rows, columns) from the matrix stored in
        the given file.
    """
    with open(file_path, 'rb') as f:
        rows = struct.unpack('<i', f.read(4))[0]
        cols = struct.unpack('<i', f.read(4))[0]
        return rows, cols


def read_matrix(file_path: str):
    shape = read_shape(file_path)
    return numpy.memmap(file_path, mode='c', dtype='<f8',
                        shape=shape, offset=8, order='F')


def write_matrix(M, file_path: str):
    with open(file_path, 'wb') as f:
        rows, cols = M.shape
        f.write(struct.pack("<i", rows))
        f.write(struct.pack("<i", cols))
        for col in range(0, cols):
            for row in range(0, rows):
                val = M[row, col]
                f.write(struct.pack("<d", val))
