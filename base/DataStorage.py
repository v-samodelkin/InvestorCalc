# @title class DataStorage { run: "auto" }
import csv
import datetime
from typing import List, Dict

from base.Atom import Atom
from consts import Tickers, AdditionalTickers


class DataStorage:
    atoms: List[Atom] = []
    atoms_indexes: Dict[str, int] = {}

    def __init__(self):
        self.indexes_tickers = []
        self.tickers = []
        self.inflation = {}

        base = datetime.date(1980, 1, 1)
        last = datetime.date.today()
        self.dates = [base + datetime.timedelta(days=x) for x in range((last - base).days)]
        for date in self.dates:
            atom = Atom()
            atom.date = date
            self.atoms.append(atom)
            self.atoms_indexes[date.strftime("%Y-%m-%d")] = len(self.atoms) - 1

    def read_files(self):
        min_date, max_date = self.init_eth_ticker()
        print(f'ETH: {min_date}, {max_date}')
        min_date, max_date = self.init_btc_ticker()
        print(f'BTC: {min_date}, {max_date}')

        self.init_indexes_tickers()
        self.init_eth_dif_ticker()
        self.init_inflation_ticker()

    def load(self):
        print('Reading...')
        self.read_files()
        print('Readed.')

    def init(self,
             end_date=None,
             start_date=None,
             year_budget=None,
             sell_part=None,
             comission=None,
             price_of_100_power=None,
             el_for_100_power=None,
             el_cost=None,
             eth_profit_for_100_power=None,
             default_eth_dif=None,
             years_amort=None,
             amort_part=None,
             exit_price=None,
             total_budget=None,
             asic_price=None,
             asic_power=None,
             asic_el=None,
             tax=0.0,
             iis=None):
        # self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        # self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        self.start_date = start_date
        self.end_date = end_date
        self.dates = [self.start_date + datetime.timedelta(days=x) for x in
                      range(0, (self.end_date - self.start_date).days + 1)]
        self.total_days = (self.end_date - self.start_date).days
        self.year_budget = year_budget
        self.sell_part = sell_part
        self.comission = comission
        if self.year_budget is not None:
            self.daily_budget = year_budget / 365.0
        self.price_of_100_power = price_of_100_power
        if el_for_100_power is not None:
            self.el_for_100_power = el_for_100_power * 24
        self.el_cost = el_cost
        self.eth_profit_for_100_power = eth_profit_for_100_power
        self.default_eth_dif = default_eth_dif
        self.years_amort = years_amort
        self.amort_part = amort_part
        self.exit_price = exit_price
        self.total_budget = total_budget
        if self.years_amort is not None:
            self.daily_amort = 1.0 / self.years_amort / 365 * self.amort_part

        self.asic_price = asic_price
        self.asic_power = asic_power
        if asic_el is not None:
            self.asic_el = asic_el * 24

        self.tax = tax
        self.iis = iis
        self.iis_daily_income = min(year_budget / 5136.0, 1.0) * 667.68 / 365 if self.iis else 0.0

    def get_atom_index(self, date):
        return self.atoms_indexes[date.strftime("%Y-%m-%d")]

    def init_inflation_ticker(self):
        with open('data/FPCPITOTLZGUSA.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for d in reader:
                date = datetime.datetime.strptime(d[0], '%Y-%m-%d')
                inflation = float(d[1])
                self.inflation[str(date.year)] = inflation
            self.inflation["2020"] = 2.0
            self.inflation["2021"] = 2.0

    def init_eth_dif_ticker(self):
        with open('data/blocks.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            prev_index = None
            for d in reader:
                date = datetime.datetime.strptime(d[0], '%Y-%m-%d')
                dif = float(d[1])
                index = self.get_atom_index(date)
                self.atoms[index].additional[AdditionalTickers.eth_dif_ticker] = dif
                if prev_index is not None:
                    for i in range(prev_index + 1, index):
                        self.atoms[i].additional[Tickers.eth_dif_ticker] = dif
                prev_index = index

    def init_eth_ticker(self) -> (datetime.datetime, datetime.datetime):
        return self.read_gdax_single(Tickers.eth_ticker, 'data/GDAX.ETH-USD_100101_201014.txt')

    def init_btc_ticker(self) -> (datetime.datetime, datetime.datetime):
        return self.read_gdax_single(Tickers.btc_ticker, 'data/GDAX.BTC-USD_100101_201014.txt')

    def init_indexes_tickers(self):
        with open('data/mfdexport_1day_01012010_20102020.txt', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for d in reader:
                ticker = d[0]
                date = datetime.datetime.strptime(d[2], '%Y%m%d')
                value = float(d[7])
                if ticker not in self.tickers:
                    self.tickers.append(ticker)
                if ticker not in self.indexes_tickers:
                    self.indexes_tickers.append(ticker)

                index = self.get_atom_index(date)
                self.atoms[index].quotation[ticker] = value

    def read_gdax_single(self, ticker: Tickers, filename: str) -> (
    datetime.datetime, datetime.datetime):
        min_date = None
        max_date = None
        prev_index = None
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            if ticker not in self.tickers:
                self.tickers.append(ticker)
            for d in reader:
                date = datetime.datetime.strptime(d[2], '%Y%m%d')
                if min_date is None:
                    min_date = date
                max_date = date
                value = float(d[7])
                index = self.get_atom_index(date)
                self.atoms[index].quotation[ticker] = value
                if prev_index is not None:
                    for i in range(prev_index + 1, index):
                        self.atoms[i].quotation[ticker] = value
                prev_index = index

        return min_date, max_date
