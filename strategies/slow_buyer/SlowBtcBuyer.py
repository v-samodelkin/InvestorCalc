from typing import List

from ipywidgets import interactive
from plotly.subplots import make_subplots

from base.Atom import Atom
from base.DataStorage import DataStorage
from consts import Strategies, Tickers, GRAPHS_FOLDER
from drawers.base.Drawer import Drawer
from strategies.drawable import DrawableStrategy
from widgets import year_budget_widget, get_comission_widget, get_skip_widget, get_date_widget


class SlowBtcBuyer(DrawableStrategy):
    daily_budget: float
    comission: float

    def __init__(self):
        self.strategy_name = Strategies.slow_btc_buyer

    def get_widget(self):
        return interactive(
            self.process,
            {'manual': True},
            year_budget=year_budget_widget,
            comission=get_comission_widget(),
            skip=get_skip_widget(value=0.33),
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
        )

    def process(self, start_date, end_date, year_budget, comission, skip):
        self.daily_budget = year_budget / 365.0
        self.comission = comission

        self.load(first=start_date, last=end_date)
        self.calc()
        self._draw(skip=skip)

    def _step(self, atoms: List[Atom], index: int):
        strategy = atoms[index].get_strategy(self.strategy_name)
        prev_strategy = atoms[index - 1].get_strategy(self.strategy_name)

        strategy.crypto_count = self.daily_budget / atoms[index].quotation[Tickers.btc_ticker] * (1 - self.comission)
        strategy.crypto_mined = strategy.crypto_count
        strategy.invested = -self.daily_budget

        strategy.total_crypto_count = prev_strategy.total_crypto_count + strategy.crypto_count
        strategy.total_revenue = prev_strategy.total_revenue + strategy.revenue
        strategy.total_invested = prev_strategy.total_invested + strategy.invested
        strategy.total_crypto_mined = prev_strategy.total_crypto_mined + strategy.crypto_mined

        strategy.crypto_assets = strategy.total_crypto_count * atoms[index].quotation[Tickers.btc_ticker]

    def _draw(self, **kwargs):
        if not self.isDrawRequired:
            return
        if (
                kwargs['skip'] is None
        ):
            raise Exception("None params")
        drawer = Drawer(self.storage)
        fig = make_subplots(
            rows=3, cols=2,
            column_widths=[0.5, 0.5],
            row_heights=[0.5, 0.2, 0.3],
            specs=[[{}, {}],
                   [{"rowspan": 2}, {}],
                   [None, {}]],
            subplot_titles=("Итоговый баланс", "ROI", "Деньги", "BTC", "Статистика портфеля BTC")
        )
        drawer.print_balance_data(self, kwargs['skip'], fig, 1, 1)
        drawer.print_money_data(self, fig, 2, 1)
        drawer.print_btc_all(self, fig, 2, 2)
        drawer.print_crypto_count(self, fig, 3, 2)
        fig.write_html(GRAPHS_FOLDER + 'slow_buyer_btc.html', auto_open=True)



