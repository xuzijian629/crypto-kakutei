from typing import Dict, List, Tuple


class PeriodicAveraged:
    def __init__(self, currency_name: str) -> None:
        self.currency = currency_name
        # key: year, value: list of (rate, amount)
        self.buy_history: Dict[int, List[Tuple[float, float]]] = {}
        self.sell_history: Dict[int, List[Tuple[float, float]]] = {}
        # key: year, value: accumulated charge
        self.charge_history: Dict[int, float] = {}
        self.computed = False

    def maybe_make_key(self, year: int) -> None:
        if year not in self.buy_history:
            self.buy_history[year] = []
        if year not in self.sell_history:
            self.sell_history[year] = []
        if year not in self.charge_history:
            self.charge_history[year] = 0.0

    def register_buy(
        self, year: int, rate: float, amount: float, jpy_charge: float = 0.0
    ) -> None:
        self.maybe_make_key(year)
        self.buy_history[year].append((rate, amount))
        self.charge_history[year] += jpy_charge

    def register_sell(
        self, year: int, rate: float, amount: float, jpy_charge: float = 0.0
    ) -> None:
        self.maybe_make_key(year)
        self.sell_history[year].append((rate, amount))
        self.charge_history[year] += jpy_charge

    def _compute(self) -> None:
        assert self.charge_history, "History is empty."
        first_year = sorted(self.charge_history.keys())[0]
        final_year = sorted(self.charge_history.keys())[-1]
        for year in range(first_year, final_year):
            self.maybe_make_key(year)

        averaged_prices: Dict[int, float] = {}
        profits: Dict[int, float] = {}
        averaged_price = 0.0
        total_amount = 0.0
        for year in range(first_year, final_year + 1):
            profit = 0.0
            buy_sum = averaged_price * total_amount
            buy_amount = 0.0
            for rate, amount in self.buy_history[year]:
                buy_sum += rate * amount
                buy_amount += amount
            sell_amount = 0.0
            for rate, amount in self.sell_history[year]:
                profit += rate * amount
                sell_amount += amount

            assert total_amount + buy_amount > 0
            averaged_price = buy_sum / (total_amount + buy_amount)
            for _, amount in self.sell_history[year]:
                profit -= averaged_price * amount
            profit -= self.charge_history[year]

            total_amount += buy_amount - sell_amount
            averaged_prices[year] = averaged_price
            profits[year] = profit

        self.averaged_prices = averaged_prices
        self.profits = profits

    def get_profits(self) -> Dict[int, float]:
        if not self.computed:
            self._compute()
        return self.profits
