from typing import List, Union, Dict

from ipywidgets import interactive
from plotly.subplots import make_subplots

from base.Atom import Atom
from base.DataStorage import DataStorage
from consts import Strategies, Tickers, GRAPHS_FOLDER
from drawers.base.Drawer import Drawer
from strategies.base import BaseStrategy
from strategies.drawable import DrawableStrategy
from strategies.slow_buyer.TickerBuyer import TickerBuyer
from widgets import *


class AllTickersBuyer(DrawableStrategy):
    daily_budget: float
    comission: float
    tax: float
    iis: bool
    iis_daily_income: float
    indexes_rois: Dict[str, List[Union[float, int]]]
    strategies: Dict[str, BaseStrategy]

    def __init__(self):
        self.strategy_name = Strategies.slow_all_indexes_buyer
        self.indexes_rois = {}
        self.strategies = {}

    def get_widget(self):
        return interactive(
            self.process,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2010),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(value=0.02),
            skip=get_skip_widget(value=0.33),
            tax=get_tax_widget(),
            iis=get_iis_widget(value=False),
        )

    def process(self,
                start_date,
                end_date,
                year_budget,
                comission,
                skip,
                tax,
                iis):
        self.daily_budget = year_budget / 365.0
        self.comission = comission
        self.tax = tax
        self.iis = iis
        self.iis_daily_income = min(year_budget / 5136.0, 1.0) * 667.68 / 365 if self.iis else 0.0

        self.load(first=start_date, last=end_date)

        for ticker in self.storage.indexes_tickers:
            strategy = TickerBuyer()
            self.strategies[ticker] = strategy
            strategy.isDrawRequired = False
            strategy.process(
                ticker,
                start_date,
                end_date,
                year_budget,
                comission,
                skip,
                tax,
                iis
            )
            cm, roi_exit, _ = strategy.calc_continues_minus()
            self.indexes_rois[ticker] = roi_exit
        self._draw(skip=skip)

    def _step(self, atoms: List[Atom], index: int):
        pass

    def _draw(self, **kwargs):
        if (
                kwargs['skip'] is None
        ):
            raise Exception("None params")
        drawer = Drawer(self.storage)

        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=("Индексы",)
        )
        drawer.print_indexes_data(self, fig, 1, 1, normalize=False)
        fig.write_html(GRAPHS_FOLDER + 'slow_buyer_indexes_full.html', auto_open=True)

        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=("Индексы",)
        )
        drawer.print_indexes_data(self, fig, 1, 1, normalize=True)
        fig.write_html(GRAPHS_FOLDER + 'slow_buyer_indexes_normalize.html', auto_open=True)

        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=("Индексы",)
        )
        drawer.print_indexes_roi(self, fig, 1, 1, skip=kwargs['skip'])
        fig.write_html(GRAPHS_FOLDER + 'slow_buyer_indexes_rois.html', auto_open=True)

        print('Done')


