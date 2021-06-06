from drawers.base.CryptoDrawer import CryptoDrawer
from drawers.base.MoneyDrawer import MoneyDrawer


class Drawer(MoneyDrawer, CryptoDrawer):

    def __init__(self, storage):
        super().__init__(storage)
