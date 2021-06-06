import plotly.graph_objects as go

from base.DataStorage import DataStorage
from strategies.base import BaseStrategy

EPS = 1e-9


def add_to_fig(days, cur, fig, name, group, row, col):
    fig.add_trace(go.Scatter(
        x=days, y=cur,
        mode='lines',
        stackgroup=group,
        name=name
    ), row=row, col=col)


class MoneyDrawer:
    storage: DataStorage

    def __init__(self, storage):
        self.storage = storage

    def print_money_data(self, strategy: BaseStrategy, fig, row, col):
        start_index, end_index = strategy.get_strategy_indexes()
        atoms = self.storage.atoms[start_index:end_index]
        days = strategy.dates

        # Инвестиции
        cur = [v.strategies[strategy.strategy_name].total_invested
               for v in atoms]
        name = "Инвестиции"
        group = "one"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Электричество
        cur = [v.strategies[strategy.strategy_name].total_elictricity_price
               for v in atoms]
        name = "Электричество"
        group = "one"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Обслуживание
        cur = [v.strategies[strategy.strategy_name].total_amort
               for v in atoms]
        name = "Обслуживание"
        group = "one"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Инфляция
        cur = [v.strategies[strategy.strategy_name].total_inflation_loss
               for v in atoms]
        name = "Инфляция"
        group = "one"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Налоги
        cur = [v.strategies[strategy.strategy_name].exit_tax
               for v in atoms]
        name = "Налоги"
        group = "one"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Доход в кэше
        cur = [v.strategies[strategy.strategy_name].total_revenue
               for v in atoms]
        name = "Доход в кэше"
        group = "two"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Сброс крипты
        cur = [v.strategies[strategy.strategy_name].crypto_assets
               for v in atoms]
        name = "Сброс 'активов'"
        group = "two"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Сброс мощностей
        cur = [v.strategies[strategy.strategy_name].power_assets
               for v in atoms]
        name = "Сброс мощностей"
        group = "two"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

        # Доход от ИИС
        cur = [v.strategies[strategy.strategy_name].total_iis_income
               for v in atoms]
        name = "Доход от ИИС"
        group = "two"
        ma = max(cur)
        mi = min(cur)
        if abs(ma) > EPS or abs(mi) > EPS:
            add_to_fig(days, cur, fig, name, group, row, col)
        else:
            print('Skip: ', name)

    # @staticmethod
    # def print_result_to_invested(days, atoms, fig, row, col):
    #     graph = go.Scatter(x=days, y=[0 for i in range(len(atoms))],
    #                        mode='lines',
    #                        name='0')
    #     fig.add_trace(graph, row=row, col=col)
    #
    #     graph = go.Scatter(x=days, y=[- v.total_balance() / v.total_invested for v in atoms],
    #                        mode='lines',
    #                        name='Отношение портфеля к вложениям')
    #     fig.add_trace(graph, row=row, col=col)
    #

    def print_balance_data(self, strategy: BaseStrategy, skip: float, fig, row, col):
        cm, roi_exit, roi_exit_inflation = strategy.calc_continues_minus()
        start_index, end_index = strategy.get_strategy_indexes()
        atoms = self.storage.atoms[start_index:end_index]
        for i in range(int(strategy.total_days * skip)):
            roi_exit[i] = 0.0
            roi_exit_inflation[i] = 0.0
        days = strategy.dates
        graph = go.Scatter(x=days, y=[0 for i in range(len(atoms))],
                           mode='lines',
                           name='0')
        fig.add_trace(graph, row=row, col=col)
        fig.add_trace(graph, row=row, col=col + 1)

        graph = go.Scatter(x=days, y=cm, mode="lines", name="Лет*доллар вложено")
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=[v.strategies[strategy.strategy_name].total_balance() + v.strategies[strategy.strategy_name].exit_tax
                                      for v in atoms],
                           mode="lines",
                           name="Прибыль выхода")
        fig.add_trace(graph, row=row, col=col)

        graph = go.Scatter(x=days, y=[v.strategies[strategy.strategy_name].total_revenue + v.strategies[strategy.strategy_name].total_minus()
                                      for v in atoms],
                           mode="lines",
                           name="Прибыль чистая")
        fig.add_trace(graph, row=row, col=col)

        ####################################################################################

        graph = go.Scatter(x=days, y=roi_exit,
                           mode="lines",
                           name="ROI выхода")
        fig.add_trace(graph, row=row, col=col + 1)

        graph = go.Scatter(x=days, y=roi_exit_inflation,
                           mode="lines",
                           name="ROI выхода с инфляцией")
        fig.add_trace(graph, row=row, col=col + 1)

        graph = go.Scatter(x=days, y=[(0
                                       if abs(v.strategies[strategy.strategy_name].total_minus()) < EPS
                                       else - v.strategies[strategy.strategy_name].total_balance() / v.strategies[
            strategy.strategy_name].total_minus())
                                      for v in atoms],
                           mode="lines",
                           name="Прибыль выхода")
        fig.add_trace(graph, row=row, col=col + 1)

        graph = go.Scatter(x=days, y=[(0
                                       if abs(v.strategies[strategy.strategy_name].total_minus()) < EPS
                                       else - (
                v.strategies[strategy.strategy_name].total_revenue + v.strategies[strategy.strategy_name].total_minus()) / v.strategies[
                                                strategy.strategy_name].total_minus())
                                      for v in atoms],
                           mode="lines",
                           name="Прибыль чистая")
        fig.add_trace(graph, row=row, col=col + 1)
