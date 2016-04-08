import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import openio.validation as validation


class Module(object):
    """
    The economic module contains the input-output data which may are hybridized
    with physical flows.
    """

    def __init__(self, use_table: pd.DataFrame, make_table: pd.DataFrame):
        """
        Creates a new instance of an economic module with the given data.

        :param use_table: the use table of the economic module
        :param make_table: the make table of the economic module
        """
        self.use_table = use_table
        self.make_table = make_table

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
        fd_share = len(self.get_final_demands()) / len(ut.columns)
        va_share = len(self.get_added_values()) / len(ut.index)

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
        for com in self.get_commodities():
            com_x.append(make_com_totals[com])
            com_y.append(use_com_totals[com])
        for ind in self.get_industries():
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

    def get_final_demands(self) -> list:
        """
        The use table contains in the columns the industry sectors and final
        demand sectors. The make table contains in the rows the industry
        sectors. Thus, the sectors in the use table columns that are not
        contained in the make table rows are the final demand sectors.
        """
        is_industry = {}
        for ind in self.make_table.index:
            is_industry[ind] = True
        final_demands = []
        for ind in self.use_table.columns:
            if ind not in is_industry:
                final_demands.append(ind)
        return final_demands

    def get_added_values(self) -> list:
        """
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

    def get_commodities(self) -> list:
        """
        Returns a list which contains the commodities from the make and use
        tables.
        """
        in_use = {}
        for com in self.use_table.index:
            in_use[com] = True
        commodities = []
        for com in self.make_table.columns:
            if com in in_use:
                commodities.append(com)
        return commodities

    def get_industries(self) -> list:
        """
        Returns a list with the industry sectors from the make and use tables.
        """
        in_use = {}
        for ind in self.use_table.columns:
            in_use[ind] = True
        industries = []
        for ind in self.make_table.index:
            if ind in in_use:
                industries.append(ind)
        return industries

    def check(self) -> validation.Validation:
        """
        Does the following checks and throws an exception if one of these fails:

        * Are all industries and commodities of the make table also contained in
          the use table? The make table should not contain 'value added' and
          'final demand' sectors so that each entry of the row and column index
          of the make table should be in contained in the respective index of
          the use table.
        """
        val = validation.Validation('Validation of economic module')
        use_com, use_ind = {}, {}
        for com in self.use_table.index:
            use_com[com] = True
        for ind in self.use_table.columns:
            use_ind[ind] = True
        for com in self.make_table.columns:
            if com not in use_com:
                val.error("Commodity '" + com + "' is contained " +
                          "in the make table but not in the use" +
                          " table")
        for ind in self.make_table.index:
            if ind not in use_ind:
                val.error("Industry '" + ind + "' is contained in the " +
                          "make table but not in the use table")
        return val
