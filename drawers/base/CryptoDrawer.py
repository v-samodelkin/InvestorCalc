import plotly.graph_objects as go

from base.DataStorage import DataStorage
from consts import AdditionalTickers, Tickers
from strategies.base import BaseStrategy


class CryptoDrawer:
    storage: DataStorage

    def __init__(self, storage):
        self.storage = storage

    def print_eth_all(self, strategy: BaseStrategy, fig, row, col):
        start_index, end_index = strategy.get_strategy_indexes(additional=AdditionalTickers.eth_dif_ticker, quotation=Tickers.eth_ticker)
        atoms = self.storage.atoms[start_index:end_index]
        days = strategy.dates

        graph = go.Scatter(x=days, y=[0 for i in range(strategy.total_days)],
                           mode='lines',
                           name='0')
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=[v.quotation[Tickers.eth_ticker] for v in atoms],
                           mode="lines",
                           name="Курс eth")
        fig.add_trace(graph, row=row, col=col)

        maxdif = max([v.additional[AdditionalTickers.eth_dif_ticker] for v in atoms])
        maxval = max([v.quotation[Tickers.eth_ticker] for v in atoms])
        graph = go.Scatter(x=days, y=[v.additional[AdditionalTickers.eth_dif_ticker] / maxdif * maxval for v in atoms], mode="lines",
                           name="Сложность эфира")
        fig.add_trace(graph, row=row, col=col)

    def print_btc_all(self, strategy: BaseStrategy, fig, row, col):
        start_index, end_index = strategy.get_strategy_indexes(quotation=Tickers.btc_ticker)
        atoms = self.storage.atoms[start_index:end_index]
        days = strategy.dates

        graph = go.Scatter(x=days, y=[0 for i in range(len(days))],
                           mode='lines',
                           name='0')
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=[v.quotation[Tickers.btc_ticker] for v in atoms],
                           mode="lines",
                           name="Курс btc")
        fig.add_trace(graph, row=row, col=col)
    #
    # @staticmethod
    # def print_eth_dif(fig, row, col):
    #     start_index, end_index = data.get_strategy_indexes()
    #     atoms = data.atoms[start_index:end_index]
    #     days = data.dates
    #     graph = go.Scatter(x=days, y=[0 for i in range(len(days))],
    #                        mode='lines',
    #                        name='0')
    #     fig.add_trace(graph, row=row, col=col)
    #
    #     graph = go.Scatter(x=days, y=[v.quotation[eth_ticker] / v.additional[eth_dif_ticker] for v in atoms],
    #                        mode="lines",
    #                        name="Отношение курса к сложности")
    #     fig.add_trace(graph, row=row, col=col)
    #
    def print_crypto_count(self, strategy: BaseStrategy, fig, row, col):
        start_index, end_index = strategy.get_strategy_indexes()
        atoms = self.storage.atoms[start_index:end_index]
        days = strategy.dates

        graph = go.Scatter(x=days, y=[0 for i in range(len(days))],
                           mode='lines',
                           name='0')
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=[v.strategies[strategy.strategy_name].total_crypto_count for v in atoms],
                           mode='lines',
                           name='"Активов" в портфеле')
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=[v.strategies[strategy.strategy_name].total_crypto_mined for v in atoms],
                           mode='lines',
                           name='"Активов" добыто')
        fig.add_trace(graph, row=row, col=col)
