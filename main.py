import datetime

from drawers.draw_slow_eth_buyer import draw_slow_eth_buyer

from base.DataStorage import DataStorage
from drawers.base.Drawer import Drawer
from strategies.slow_buyer.SlowEthBuyer import SlowEthBuyer

storage = DataStorage()
storage.load()
a = 2

base = datetime.date(2018, 10, 10)
last = datetime.date(2020, 10, 10)

strategy = SlowEthBuyer(daily_budget=10000.0/365, comission=0.05, storage=storage, first=base, last=last)
strategy.calc()

drawer = Drawer(storage)

draw_slow_eth_buyer(drawer, strategy, 0.33)

