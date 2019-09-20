import csv
import os
import struct

import iomb
import iomb.dqi as dqi
import numpy
import logging as log
import pandas as pd


class Matrices(object):
    """A collection of model matrices with methods to export for API and to csv"""

    def __init__(self, model, DQImatrices=False):
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
                self.U_dqi = self.D_dqi.aggregate_mmult(self.D.values, self.L.values, left=True)
                self.dqi_matrices['U_dqi'] = self.U_dqi
            except KeyError:
                log.warning('U_dqi could not be computed.')

    def export_to_csv(self, folder: str, exportDQImatrices=False):
        """Exports all matrices in formatted csv files

        :param folder: path to export folder
        :param exportDQImatrices: True/False, whether to include DQI matrices in export
        :return:
        """
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        for k, v in self.component_matrices.items():
            v.to_csv(folder + k +'.csv')

        for k, v in self.result_matrices.items():
            v.to_csv(folder + k +'.csv')

        if exportDQImatrices:
            if 'B_dqi' in self.dqi_matrices:
                df = dqi_matrix_to_df(self.B_dqi,self.B.index, self.B.columns)
                df.to_csv(folder+'B_dqi.csv')
            if 'D_dqi' in self.dqi_matrices:
                df = dqi_matrix_to_df(self.D_dqi, self.D.index, self.D.columns)
                df.to_csv(folder + 'D_dqi.csv')
            if 'U_dqi' in self.dqi_matrices:
                df = dqi_matrix_to_df(self.U_dqi, self.U.index, self.U.columns)
                df.to_csv(folder + 'U_dqi.csv')

    def export_for_api(self, folder: str, exportDQImatrices=False):
        """ Exports the matrices of the model in formats for the API to the given folder.

            Args:
                folder (str): the path to the export folder
        """
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)

        for k, v in self.component_matrices.items():
            self.__write_matrix(v.values, k)

        for k, v in self.result_matrices.items():
            self.__write_matrix(v.values, k)

        if exportDQImatrices:
            for k, v in self.dqi_matrices.items():
                v.to_csv(folder+k+'.csv')

        # write matrix indices with meta-data
        self.__write_sectors(self.A)
        self.__write_flows(self.B)
        self.__write_indicators(self.C)

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


def dqi_matrix_to_df(dqi_matrix, new_index, new_columns):
    """Converts a DQI matrix to csv
    :param dqi_matrix: a matrix from model.matrices.dqi_matrices
    :param new_index: a list for using as an index
    :param new_columns: a list for columns
    :return: a pandas df of the matrix
    """
    # Use matrices existing 'to_csv' function for lack of quicker wat
    dqi_matrix.to_csv('temp_dqi.csv')
    dqi_df = pd.read_csv('temp_dqi.csv', header=None, index_col=False)
    os.remove('temp_dqi.csv')
    dqi_df.index = new_index
    dqi_df.columns = new_columns
    return dqi_df


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
