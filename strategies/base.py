import datetime
from abc import abstractmethod, ABC
from typing import List

from base.DataStorage import DataStorage
from base.StrategyData import StrategyData
from consts import Strategies


class BaseStrategy(ABC):
    dates: List[datetime.date]
    strategy_name: Strategies
    storage: DataStorage
    total_days: int
    ticker: str
    isDrawRequired = True

    def load(self, first: datetime.date = None, last: datetime.date = None):
        if (
                first is None or
                last is None
        ):
            raise Exception("None params")
        self.storage = DataStorage()
        self.storage.load()
        self.dates = [first + datetime.timedelta(days=x) for x in range((last - first).days)]
        self.total_days = len(self.dates)

        prev_atom_inflation = 1.0
        for date in self.dates:
            index = self.storage.get_atom_index(date)
            self.storage.atoms[index].inflation = pow(self.storage.inflation[date.strftime("%Y")] / 100.0 + 1.0,
                                                      1.0 / 365) * prev_atom_inflation

            prev_atom_inflation = self.storage.atoms[index].inflation
        for date in self.dates:
            index = self.storage.get_atom_index(date)
            if self.strategy_name not in self.storage.atoms[index].strategies:
                self.storage.atoms[index].strategies[self.strategy_name] = StrategyData()
            if self.strategy_name not in self.storage.atoms[index - 1].strategies:
                self.storage.atoms[index - 1].strategies[self.strategy_name] = StrategyData()

    def calc(self, start_date=0):
        for date in self.dates[start_date:]:
            index = self.storage.get_atom_index(date)
            self._step(self.storage.atoms, index)

    @abstractmethod
    def _step(self, atoms, index):
        pass

    def get_strategy_indexes(self, quotation=None, additional=None):
        start_index = self.storage.get_atom_index(self.dates[0])
        end_index = self.storage.get_atom_index(self.dates[-1])
        for i in range(start_index, end_index):
            if self.strategy_name not in self.storage.atoms[i].strategies:
                print(self.storage.atoms[i].strategies)
                raise Exception(f'{i} doesn\'t contains {self.strategy_name} ({self.storage.atoms[i].date})')
        if quotation is not None:
            for i in range(start_index, end_index):
                if quotation not in self.storage.atoms[i].quotation:
                    print(self.storage.atoms[i].quotation)
                    raise Exception(f'{i} doesn\'t contains {quotation} ({self.storage.atoms[i].date})')
        if additional is not None:
            for i in range(start_index, end_index):
                if additional not in self.storage.atoms[i].additional:
                    print(self.storage.atoms[i].additional)
                    raise Exception(f'{i} doesn\'t contains {additional} ({self.storage.atoms[i].date})')

        return start_index, end_index

    def calc_continues_minus(self):
        cm = [0.0]
        roi_exit = [0.0]
        roi_exit_inflation = [0.0]
        i = 0
        # dates = tqdm(self.dates, desc=f'Считаю roi {strategy}') if SHOW_BAR_FOR_INDEX else self.dates
        for date in self.dates:  # self.dates:
            i += 1
            index = self.storage.get_atom_index(date)
            cmi = 0.0
            total_inlfation_lose = 0.0
            for j in range(i):
                calc_index = index - j
                cmi += self.storage.atoms[calc_index].strategies[
                    self.strategy_name].total_minus()  # Сколько долларо-часов вложено всего
                invested = -self.storage.atoms[calc_index].strategies[self.strategy_name].invested
                inflation = self.storage.atoms[calc_index].inflation
                total_inlfation_lose += -(invested - invested / inflation)
            total_invested = -self.storage.atoms[index].strategies[self.strategy_name].total_invested
            inflation = self.storage.atoms[index].inflation
            self.storage.atoms[index].strategies[self.strategy_name].total_inflation_loss = total_inlfation_lose
            cm.append(cmi / 365.0)  # долларо-лет вложено всего
            if cm[-1] != 0:
                balance = self.storage.atoms[index].strategies[self.strategy_name].total_balance() + \
                          self.storage.atoms[index].strategies[
                              self.strategy_name].exit_tax
                roi_exit.append(- balance / cm[-1])
                roi_exit_inflation.append(-(balance + total_inlfation_lose) / cm[-1])
            else:
                roi_exit.append(0)
                roi_exit_inflation.append(0)
        return cm, roi_exit, roi_exit_inflation
