from ipywidgets import interactive
from plotly.subplots import make_subplots

from consts import Tickers, Strategies, ETH_PROFIT_FOR_100_POWER, DEFAULT_ETH_DIF, GRAPHS_FOLDER, AdditionalTickers
from drawers.base.Drawer import Drawer
from strategies.drawable import DrawableStrategy
from widgets import *


class CardsMinerEth(DrawableStrategy):
    daily_budget: float
    comission: float
    sell_part: float
    asic_price: float
    asic_power: float
    asic_el: float
    el_cost: float
    daily_amort: float
    amort_part: float
    exit_price: float

    def __init__(self):
        self.strategy_name = Strategies.miner_cards_eth

    def get_widget(self):
        return interactive(
            self.process,
            {'manual': True},
            start_date=get_date_widget(text="Дата начала", year=2018),
            end_date=get_date_widget(text="Дата окончания", year=2020),
            year_budget=year_budget_widget,
            comission=get_comission_widget(),
            sell_part = get_sell_part_widget(max=1.0, value=0.9),
            skip=get_skip_widget(value=0.5),
            asic_price = asic_price_widget,
            asic_power = asic_power_widget,
            asic_el = asic_el_widget,
            el_cost = el_cost_widget,
            years_amort = years_amort_widget,
            amort_part = amort_part_widget,
            exit_price = exit_price_widget,
        )

    def process(self,
                start_date=None,
                end_date=None,
                year_budget=None,
                comission=None,
                sell_part=None,
                skip=None,
                asic_price=None,
                asic_power=None,
                asic_el=None,
                el_cost=None,
                years_amort=None,
                amort_part=None,
                exit_price=None):
        self.daily_budget = year_budget / 365.0
        self.comission = comission
        self.sell_part = sell_part
        self.asic_price = asic_price
        self.asic_power = asic_power
        if asic_el is not None:
            self.asic_el = asic_el * 24
        self.el_cost = el_cost
        self.daily_amort = 1.0 / years_amort / 365 * amort_part
        self.amort_part = amort_part
        self.exit_price = exit_price

        self._free_money = 0

        self.load(first=start_date, last=end_date)
        self.calc()
        self._draw(skip=skip)

    def _step(self, atoms, index):
        strategy = atoms[index].get_strategy(self.strategy_name)
        prev_strategy = atoms[index - 1].get_strategy(self.strategy_name)

        self._free_money += self.daily_budget
        invested = 0.0
        if self._free_money >= self.asic_price:
            asics = int(self._free_money / self.asic_price)
            strategy.bought_power = self.asic_power * asics
            self._free_money -= self.asic_price * asics
            invested = -self.asic_price * asics
        strategy.total_bought_power = prev_strategy.total_bought_power + strategy.bought_power

        strategy.elictricity_price = -strategy.total_bought_power / self.asic_power * self.asic_el * self.el_cost
        strategy.total_elictricity_price = prev_strategy.total_elictricity_price + strategy.elictricity_price

        strategy.invested = invested
        strategy.total_invested = prev_strategy.total_invested + strategy.invested

        strategy.crypto_mined = strategy.total_bought_power / 100 * ETH_PROFIT_FOR_100_POWER * (
                    DEFAULT_ETH_DIF / atoms[index].additional[AdditionalTickers.eth_dif_ticker])
        strategy.total_crypto_mined = prev_strategy.total_crypto_mined + strategy.crypto_mined

        strategy.total_crypto_count = prev_strategy.total_crypto_count + strategy.crypto_mined
        sold_eth = strategy.crypto_mined * self.sell_part
        strategy.crypto_count = strategy.crypto_mined - sold_eth
        strategy.total_crypto_count = strategy.total_crypto_count - sold_eth

        strategy.revenue = sold_eth * atoms[index].quotation[Tickers.eth_ticker]
        strategy.total_revenue = prev_strategy.total_revenue + strategy.revenue

        strategy.amort = strategy.total_invested * self.daily_amort
        strategy.total_amort = prev_strategy.total_amort + strategy.amort

        strategy.crypto_assets = strategy.total_crypto_count * atoms[index].quotation[Tickers.eth_ticker]
        strategy.power_assets = -strategy.total_invested * self.exit_price

    def _draw(self, **kwargs):
        if (
                kwargs['skip'] is None
        ):
            raise Exception("None params")
        fig = make_subplots(
            rows=3, cols=2,
            column_widths=[0.5, 0.5],
            row_heights=[0.5, 0.2, 0.3],
            specs=[[{}, {}],
                   [{"rowspan": 2}, {}],
                   [None, {}]],
            subplot_titles=("Итоговый баланс", "ROI", "Деньги", "Эфир", "Статистика портфеля Эфира")
        )
        drawer = Drawer(self.storage)

        drawer.print_balance_data(self, kwargs['skip'], fig, 1, 1)
        drawer.print_money_data(self, fig, 2, 1)

        drawer.print_eth_all(self, fig, 2, 2)
        drawer.print_crypto_count(self, fig, 3, 2)

        fig.write_html(GRAPHS_FOLDER + 'miner_eth.html', auto_open=True)
        print('Done')

