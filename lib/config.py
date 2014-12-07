from lib.screens.balances import BalancesScreen
from lib.screens.dex import DexScreen
from lib.screens.contracts import ContractsScreen

class Config:
    def __init__(self, args=None):
        self.args = args
        self.screenClassList = [BalancesScreen, DexScreen, ContractsScreen]
