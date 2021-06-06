import datetime
from abc import ABC, abstractmethod

from ipywidgets import interactive

from base.DataStorage import DataStorage
from consts import Strategies
from strategies.base import BaseStrategy


class DrawableStrategy(BaseStrategy, ABC):
    @abstractmethod
    def get_widget(self):
        pass

    @abstractmethod
    def process(self, **kwargs):
        pass

    @abstractmethod
    def _draw(self, **kwargs):
        pass
