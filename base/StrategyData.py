class StrategyData:
    # Основные величины
    revenue: float = 0.0  # доход
    iis_income: float = 0.0  # доход от ИИС
    invested: float = 0.0  # основные затраты
    elictricity_price: float = 0.0  # затраты на электричество
    amort: float = 0.0  # затраты на поддержку оборудования

    # Вспомогательные величины
    crypto_count: float = 0.0  # дельта эфира на руках
    crypto_mined: float = 0.0  # сколько эфира намайнено
    bought_power: float = 0.0  # мощность майнинга

    # Обобщающие величины
    # - Основные
    # -- Plus
    crypto_assets: float = 0.0  # "активы" для сброса
    power_assets: float = 0.0  # "активы" для сброса
    total_revenue: float = 0.0
    total_iis_income: float = 0.0  # доход от ИИС
    total_inflation_loss: float = 0.0  # общие потери от инфляции
    # -- Minus
    total_invested: float = 0.0
    total_elictricity_price: float = 0.0
    total_amort: float = 0.0
    exit_tax: float = 0.0
    # - Вспомогательные
    total_crypto_count: float = 0.0
    total_crypto_mined: float = 0.0
    total_bought_power: float = 0.0

    def total_plus(self) -> float:
        return self.crypto_assets + self.power_assets + self.total_revenue + self.total_iis_income

    def total_minus(self) -> float():
        return self.total_invested + self.total_elictricity_price + self.total_amort

    def minus(self) -> float():
        return self.invested + self.elictricity_price + self.amort

    def total_balance(self) -> float:
        return self.total_plus() + self.total_minus()

    def total_assest(self) -> float:
        return self.crypto_assets + self.power_assets
