from enum import Enum
from typing import Dict

GRAPHS_FOLDER = 'output/'

DEFAULT_ETH_DIF = 3403254863879692.0
ETH_PROFIT_FOR_100_POWER = 0.0075

class Strategies(Enum):
    slow_eth_buyer = "Slow ETH Buyer"
    slow_btc_buyer = "Slow BTC Buyer"
    miner_eth = "Miner ETH"
    miner_once_eth = "Miner once ETH"
    miner_cards_eth = "Miner cards ETH"
    slow_index_buyer = "Slow Indexes Buyer"


StrategiesHeaders: Dict[str, Strategies] = {
    '[ETH] Закупаем вечно': Strategies.slow_eth_buyer,
    '[ETH] Закупаем мощность': Strategies.miner_eth,
    '[ETH] Купили мощность разово': Strategies.miner_once_eth,
    '[ETH] Закупаем Асики/Видеокарты': Strategies.miner_cards_eth,
    '[BTC] Закупаем вечно': Strategies.slow_btc_buyer,
    'Покупаем индекс': Strategies.slow_index_buyer,
}


# options=['Просто покажи данные',
#          '[ETH] Закупаем вечно',
#          '[ETH] Закупаем мощность',
#          '[ETH] Купили мощность разово',
#          '[ETH] Закупаем Асики/Видеокарты',
#          '[BTC] Закупаем вечно',
#          'Закупка индексов',
#          'Покупаем индекс'],


class Tickers(Enum):
    eth_ticker = 'ETH'
    btc_ticker = 'BTC'


class AdditionalTickers(Enum):
    eth_dif_ticker = 'ETH Difficulty'
    inflation_ticker = 'Inflation'

# from __future__ import print_function
# from ipywidgets import interact, interactive, fixed, interact_manual
# import ipywidgets as widgets
# from IPython.display import display
#
# def f(x):
#     w = interact_manual(f, x=10)
#     display(w)
#     return x
#
# w = interact_manual(f, x=10)
#
# display(w)
