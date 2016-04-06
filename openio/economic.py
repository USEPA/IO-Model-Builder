import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


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
        fig = plt.figure(figsize=(4, 4))
        sub = fig.add_subplot(111, aspect='equal')

        rect = patches.Rectangle((0, 0.2), 0.8, 0.8, facecolor='#409f9c',
                                 edgecolor='#409f9c')
        sub.add_patch(rect)
        rect = patches.Rectangle((0, 0.0), 0.8, 0.2, facecolor='#9c0000',
                                 edgecolor='#9c0000')
        sub.add_patch(rect)
        rect = patches.Rectangle((0.8, 0.2), 0.2, 0.8, facecolor='#f3ffb2',
                                 edgecolor='#f3ffb2')
        sub.add_patch(rect)

        sub.axes.get_xaxis().set_ticks([])
        sub.set_xlabel('Industries')
        sub.axes.get_yaxis().set_ticks([])
        sub.set_ylabel('Commodities')

        legend_entries = [
            patches.Patch(color='#409f9c', label='Industry inputs'),
            patches.Patch(color='#9c0000', label='Value added'),
            patches.Patch(color='#f3ffb2', label='Final demand')]
        sub.legend(handles=legend_entries, fontsize=10, loc=2)
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
