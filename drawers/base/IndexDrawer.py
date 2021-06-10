import plotly.graph_objects as go

from base.DataStorage import DataStorage
from strategies.base import BaseStrategy


class IndexDrawer:
    storage: DataStorage

    def __init__(self, storage):
        self.storage = storage

    def print_index_all(self, strategy: BaseStrategy, fig, row, col):
        start_index, end_index = strategy.get_strategy_indexes()
        atoms = self.storage.atoms[start_index:end_index]

        values = [v.external_quotation[strategy.ticker] if strategy.ticker in v.external_quotation else None for v in atoms]
        days = strategy.dates

        graph = go.Scatter(x=days, y=[0 for i in range(len(days))],
                           mode='lines',
                           name='0')
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=values, mode="lines", name="Курс " + strategy.ticker)
        fig.add_trace(graph, row=row, col=col)

    def print_indexes_data(self, master_strategy, fig, row, col, skip=0.0, normalize=False):
        for ticker in master_strategy.indexes_rois:
            strategy = master_strategy.strategies[ticker]
            start_index, end_index = strategy.get_strategy_indexes()
            atoms = strategy.storage.atoms[start_index:end_index]
            days = strategy.dates

            values = [v.external_quotation[ticker] if ticker in v.external_quotation else None for v in atoms]
            not_none_values = [v for v in values if v is not None]
            if len(not_none_values):
                if normalize:
                    maxprice = max(not_none_values)
                    prices = [v / maxprice if v is not None else None for v in values]
                else:
                    prices = values
                graph = go.Scatter(x=days, y=prices, mode="lines", name = ticker)
                fig.add_trace(graph, row=row, col=col)

    def print_indexes_roi(self, master_strategy, fig, row, col, skip=0.0, console=True):
        rois = []
        for ticker in master_strategy.indexes_rois:
            strategy = master_strategy.strategies[ticker]
            start_index, end_index = strategy.get_strategy_indexes()
            atoms = strategy.storage.atoms[start_index:end_index]
            days = strategy.dates

            values = [v.external_quotation[ticker] if ticker in v.external_quotation else None for v in atoms]
            not_none_values = [v for v in values if v is not None]
            if len(not_none_values):
                index_roi = master_strategy.indexes_rois[ticker]
                skiped = len(index_roi) * skip
                for i in range(int(skiped)):
                    index_roi[i] = 0
                graph = go.Scatter(x=days, y=index_roi, mode="lines", name = ticker)
                fig.add_trace(graph, row=row, col=col)
                rois.append((index_roi[-1], ticker))
        rois.sort(reverse=True)
        for roi, ticker in rois:
            roi = int(roi * 10000) / 100.0
            print(f'{ticker}: {roi}%')
