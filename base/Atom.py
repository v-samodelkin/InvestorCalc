import datetime
from typing import Dict

from base.StrategyData import StrategyData
from consts import Strategies, Tickers, AdditionalTickers

class Atom:
    date: datetime.date
    strategies: Dict[Strategies, StrategyData]
    additional: Dict[AdditionalTickers, float]
    quotation: Dict[Tickers, float]
    external_quotation: Dict[str, float]
    inflation: float

    def __init__(self):
        self.strategies = {}
        self.additional = {}
        self.quotation = {}
        self.external_quotation = {}
        self.inflation = 1.0

    def get_strategy(self, strategy: Strategies) -> StrategyData:
        return self.strategies[strategy]
