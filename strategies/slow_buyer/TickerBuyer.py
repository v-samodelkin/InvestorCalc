from typing import List

from ipywidgets import interactive
from plotly.subplots import make_subplots

from base.Atom import Atom
from base.DataStorage import DataStorage
from consts import Strategies, Tickers, GRAPHS_FOLDER
from drawers.base.Drawer import Drawer
from strategies.drawable import DrawableStrategy
from widgets import *


class TickerBuyer(DrawableStrategy):
    daily_budget: float
    comission: float
    tax: float
    iis: bool
    iis_daily_income: float

    def __init__(self):
        self.strategy_name = Strategies.slow_index_buyer

    def get_widget(self):
        return interactive(
            self.process,
            {'manual': True},
            ticker=get_switch_index_widget(),
            start_date=get_date_widget(text="Дата начала", year=2010),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(value=0.02),
            skip=get_skip_widget(value=0.33),
            tax=get_tax_widget(),
            iis=get_iis_widget(value=False),
        )

    def process(self,
                ticker,
                start_date,
                end_date,
                year_budget,
                comission,
                skip,
                tax,
                iis):
        self.ticker = ticker
        self.daily_budget = year_budget / 365.0
        self.comission = comission
        self.tax = tax
        self.iis = iis
        self.iis_daily_income = min(year_budget / 5136.0, 1.0) * 667.68 / 365 if self.iis else 0.0

        self.load(first=start_date, last=end_date)
        self.calc()
        self._draw(skip=skip)

    def _step(self, atoms: List[Atom], index: int):
        strategy = atoms[index].get_strategy(self.strategy_name)
        prev_strategy = atoms[index - 1].get_strategy(self.strategy_name)

        strategy.crypto_count = self.daily_budget / atoms[index].external_quotation[self.ticker] * (1 - self.comission)
        strategy.invested = -self.daily_budget

        strategy.total_crypto_count = prev_strategy.total_crypto_count + strategy.crypto_count
        strategy.total_invested = prev_strategy.total_invested + strategy.invested

        strategy.crypto_assets = strategy.total_crypto_count * atoms[index].external_quotation[self.ticker]
        balance = strategy.total_balance()
        strategy.exit_tax = -balance * self.tax if balance > 0 else 0
        strategy.iis_income = self.iis_daily_income
        strategy.total_iis_income = prev_strategy.total_iis_income + strategy.iis_income

        # self.indexes_rois = {}
        #
        # strategy_name = f'{slow_indexes_buyer}_{ticker}'
        #
        # cm, roi_exit, _ = self.calc_continues_minus()
        # self.indexes_rois[ticker] = roi_exit

    def _draw(self, **kwargs):
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
            subplot_titles=("Итоговый баланс", "ROI", "Деньги", self.ticker, "Статистика портфеля " + self.ticker)
        )
        drawer.print_balance_data(self, kwargs['skip'], fig, 1, 1)
        drawer.print_money_data(self, fig, 2, 1)

        drawer.print_index_all(self, fig, 2, 2)
        drawer.print_crypto_count(self, fig, 3, 2)
        fig.write_html(GRAPHS_FOLDER + 'slow_buyer_nas.html', auto_open=True)

