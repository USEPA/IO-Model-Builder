import pandas as pd
import logging as log
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import numpy.linalg as linalg


class Model(object):
    """
    The economic module contains the input-output data which may are hybridized
    with physical flows.
    """

    def __init__(self, use_table: pd.DataFrame, make_table: pd.DataFrame,
                 scrap_sectors=None):
        """
        Creates a new instance of an economic module with the given data.

        :param use_table: the use table of the economic module
        :param make_table: the make table of the economic module
        """
        self.use_table = use_table
        self.make_table = make_table
        self.scrap_sectors = scrap_sectors
        self._industries = None
        self._commodities = None

    def viz_use_table(self):
        """
        Creates a visualization of the shape of the use table.
        """
        fig = plt.figure(figsize=(4, 4))
        sub = fig.add_subplot(111, aspect='equal')

        ut = self.use_table
        max_size = max(len(ut.index), len(ut.columns))
        size_x = len(ut.columns) / max_size
        size_y = len(ut.index) / max_size
        fd_share = len(self.final_demand_sectors) / len(ut.columns)
        va_share = len(self.value_added_sectors) / len(ut.index)

        # industry inputs
        ind_x = 0
        ind_y = (1 - size_y) + (size_y * va_share)
        ind_w = size_x - (size_x * fd_share)
        ind_h = 1 - ind_y
        ind_col = '#409f9c'
        sub.add_patch(patches.Rectangle((ind_x, ind_y), ind_w, ind_h,
                                        facecolor=ind_col, edgecolor=ind_col))

        # value added
        va_x = 0
        va_y = 1 - size_y
        va_w = ind_w
        va_h = size_y - ind_h
        va_col = '#9c0000'
        sub.add_patch(patches.Rectangle((va_x, va_y), va_w, va_h,
                                        facecolor=va_col, edgecolor=va_col))

        # final demands
        fd_x = ind_w
        fd_y = ind_y
        fd_w = size_x - ind_w
        fd_h = ind_h
        fd_col = '#f3ffb2'
        sub.add_patch(patches.Rectangle((fd_x, fd_y), fd_w, fd_h,
                                        facecolor=fd_col, edgecolor=fd_col))

        sub.axes.get_xaxis().set_ticks([])
        sub.set_xlabel('Industries')
        sub.axes.get_yaxis().set_ticks([])
        sub.set_ylabel('Commodities')

        legend_entries = [
            patches.Patch(color=ind_col, label='Commodity inputs'),
            patches.Patch(color=va_col, label='Value added'),
            patches.Patch(color=fd_col, label='Final demand')]
        sub.legend(handles=legend_entries, fontsize=10, loc=2)
        plt.show()

    def viz_make_table(self):
        """
        Creates a visualization of the shape of the make table.
        """
        fig = plt.figure(figsize=(4, 4))
        sub = fig.add_subplot(111, aspect='equal')

        mt = self.make_table
        max_size = max(len(mt.index), len(mt.columns))
        size_x = len(mt.columns) / max_size
        size_y = len(mt.index) / max_size

        col = '#409f9c'
        sub.add_patch(patches.Rectangle((0, 1 - size_y), size_x, size_y,
                                        facecolor=col, edgecolor=col))

        sub.axes.get_xaxis().set_ticks([])
        sub.set_xlabel('Commodities')
        sub.axes.get_yaxis().set_ticks([])
        sub.set_ylabel('Industries')

        legend_entries = [
            patches.Patch(color=col, label='Commodity outputs')]
        sub.legend(handles=legend_entries, fontsize=10, loc=2)
        plt.show()

    def viz_totals(self):
        fig, (plot1, plot2) = plt.subplots(1, 2, sharex=True, sharey=True,
                                           figsize=(10, 6))
        make_com_totals = self.make_table.sum(axis=0)
        make_ind_totals = self.make_table.sum(axis=1)
        use_com_totals = self.use_table.sum(axis=1)
        use_ind_totals = self.use_table.sum(axis=0)
        ind_x, ind_y, com_x, com_y = [], [], [], []
        for com in self.commodities:
            com_x.append(make_com_totals[com])
            com_y.append(use_com_totals[com])
        for ind in self.industries:
            ind_x.append(make_ind_totals[ind])
            ind_y.append(use_ind_totals[ind])
        plt.ticklabel_format(style='sci', scilimits=(0, 0))

        plot1.set_title('Commodity totals')
        plot1.scatter(com_x, com_y)
        plot1.set_xlabel('Make table')
        plot1.set_ylabel('Use table')

        plot2.set_title('Industry totals')
        plot2.scatter(ind_x, ind_y)
        plot2.set_xlabel('Make table')
        plot2.set_ylabel('Use table')
        plt.show()

    @property
    def final_demand_sectors(self) -> list:
        """ Returns the list of final demand sectors from the model.

        The use table contains in the columns the industry sectors and final
        demand sectors. The make table contains in the rows the industry
        sectors. Thus, the sectors in the use table columns that are not
        contained in the make table rows are the final demand sectors.
        """
        is_industry = {}
        for ind in self.make_table.index:
            is_industry[ind] = True
        fds = []
        for ind in self.use_table.columns:
            if ind not in is_industry:
                fds.append(ind)
        return fds

    @property
    def value_added_sectors(self) -> list:
        """ Returns the list of value added sectors from the model.

        The use table contains in the rows commodities and value added sectors.
        The make table contains in the columns commodities. Thus, the sectors
        in the use table rows that are not contained in the make table columns
        are the added value sectors.
        """
        is_commodity = {}
        for com in self.make_table.columns:
            is_commodity[com] = True
        added_values = []
        for com in self.use_table.index:
            if com not in is_commodity:
                added_values.append(com)
        return added_values

    @property
    def commodities(self) -> list:
        """ Returns the commodities from the make and use tables. """
        if self._commodities is not None:
            return self._commodities
        in_use = {}
        for com in self.use_table.index:
            in_use[com] = True
        commodities = []
        scraps = [] if self.scrap_sectors is None else self.scrap_sectors
        for com in self.make_table.columns:
            if com in in_use and com not in scraps:
                commodities.append(com)
        commodities.sort()
        self._commodities = commodities
        return commodities

    @property
    def industries(self) -> list:
        """
        Returns a list with the industry sectors from the make and use tables.
        """
        if self._industries is not None:
            return self._industries
        in_use = {}
        for ind in self.use_table.columns:
            in_use[ind] = True
        industries = []
        for ind in self.make_table.index:
            if ind in in_use:
                industries.append(ind)
        industries.sort()
        self._industries = industries
        return industries

    def get_market_shares(self) -> pd.DataFrame:
        """
        Calculates the market shares from the make table. This method returns
        an industry*commodity matrix.
        """
        log.info('calculate market shares')
        commodity_totals = self.make_table.sum(axis=0)

        # short solution (equivalent to explicit solution below)
        # shares = self.make_table.div(commodity_totals, axis=1)
        # shares = shares.ix[self.industries, self.commodities]

        shares = self.make_table.loc[self.industries, self.commodities]
        for com in self.commodities:
            total = commodity_totals[com]
            if total == 0:
                total = 1  # avoid NaN values
            for ind in self.industries:
                share = shares.at[ind, com] / total
                shares.at[ind, com] = share
        return shares

    def get_non_scrap_ratios(self) -> pd.DataFrame:
        industries = self.industries
        title = 'Nonscrap Ratio'
        if self.scrap_sectors is None or len(self.scrap_sectors) == 0:
            data = np.ones((len(industries), 1), dtype=float)
            return pd.DataFrame(data=data, index=industries, columns=[title])
        totals = self.make_table.sum(axis=1)
        data = np.zeros(len(industries))
        ratios = pd.DataFrame(data, index=industries, columns=[title])
        for industry in industries:
            total = totals[industry]
            if total == 0:
                continue
            scrap = 0
            for s in self.scrap_sectors:
                scrap += self.make_table.at[industry, s]
            ratio = (total - scrap) / total
            ratios.at[industry, title] = ratio
        return ratios

    def get_transformation_matrix(self) -> pd.DataFrame:
        log.info('calculate transformation matrix')
        shares = self.get_market_shares()
        if self.scrap_sectors is None or len(self.scrap_sectors) == 0:
            return shares
        ratios = self.get_non_scrap_ratios()
        col = ratios.columns[0]
        for industry in shares.index:
            ratio = ratios.at[industry, col]
            for commodity in shares.columns:
                share = shares.at[industry, commodity]
                shares.at[industry, commodity] = share/ratio
        return shares

    def get_direct_requirements(self) -> pd.DataFrame:
        """
        Calculates the direct requirements table from the use table. This
        method returns a commodity*industry matrix.
        """
        log.info('calculate direct requirements')
        industry_totals = self.use_table.sum(axis=0)
        drs = self.use_table.loc[self.commodities, self.industries]
        for ind in self.industries:
            total = industry_totals[ind]
            if total == 0:
                total = 1  # avoid NaN values
            for com in self.commodities:
                dr = drs.at[com, ind] / total
                drs.at[com,ind] = dr
        return drs

    def get_dr_coefficients(self) -> pd.DataFrame:
        """
        Calculates the direct requirement coefficients from the market shares
        and direct requirements table. This method returns a
        commodity*commodity matrix.
        """
        log.info('calculate direct requirements coefficients A')
        drs = self.get_direct_requirements()
        tm = self.get_transformation_matrix()
        return drs.dot(tm)

    def get_tr_coefficients(self) -> pd.DataFrame:
        """
        Calculates the total requirements coefficients.
        """
        log.info('calculate total requirements coefficients')
        drc = self.get_dr_coefficients()
        eye = np.eye(drc.shape[0], dtype=np.float64)
        data = linalg.inv(eye - drc.as_matrix())
        return pd.DataFrame(data=data, index=drc.index, columns=drc.columns)
