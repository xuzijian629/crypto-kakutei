from typing import List

import pytest

from crykak.periodic_averaged import PeriodicAveragedSingle


class Transaction:
    def __init__(
        self, buy_or_sell: str, amount: float, jpy: float, year: int = 2021, jpy_charge: float = 0.0
    ) -> None:
        self.buy_or_sell = buy_or_sell
        self.rate = jpy / amount
        self.amount = amount
        self.year = year
        self.jpy_charge = jpy_charge

    def register_to(self, manager: PeriodicAveragedSingle) -> None:
        if self.buy_or_sell == "buy":
            manager.register_buy(self.year, self.rate, self.amount, self.jpy_charge)
        elif self.buy_or_sell == "sell":
            manager.register_sell(self.year, self.rate, self.amount, self.jpy_charge)
        else:
            raise RuntimeError(f"Invalid buy_or_sell: {self.buy_or_sell}")


History = List[Transaction]


@pytest.mark.parametrize(
    ("history", "expected"),
    [
        (
            [
                Transaction("buy", 1, 100),
                Transaction("sell", 1, 200),
            ],
            100,
        ),
        (
            [
                Transaction("buy", 1, 100),
                Transaction("sell", 0.5, 200),
            ],
            150,
        ),
        (
            [
                Transaction("buy", 1, 100),
                Transaction("sell", 0.5, 200, jpy_charge=10),
            ],
            140,
        ),
        (
            [
                Transaction("buy", 1, 100),
                Transaction("sell", 0.1, 20),
                Transaction("sell", 0.2, 50),
            ],
            40,
        ),
        (
            [
                Transaction("buy", 1, 100),
                Transaction("buy", 2, 170),
                Transaction("sell", 0.5, 200),
            ],
            155,
        ),
        (
            [
                Transaction("buy", 1, 100),
                Transaction("buy", 2, 170),
                Transaction("buy", 3, 210),
                Transaction("sell", 1, 120),
                Transaction("sell", 1.5, 200),
            ],
            120,
        ),
    ],
)
def test_periodic_averaged_same_year(history: History, expected: float) -> None:
    manager = PeriodicAveragedSingle("test")
    for transaction in history:
        transaction.register_to(manager)
    profit = manager.get_profits()
    assert profit[list(profit)[0]] == expected
