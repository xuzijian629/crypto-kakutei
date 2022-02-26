from typing import Dict, List

import pytest

from crykak.periodic_averaged import PeriodicAveragedSingle

DEFAULT_YEAR = 2021


class Transaction:
    def __init__(
        self,
        buy_or_sell: str,
        amount: float,
        jpy: float,
        year: int = DEFAULT_YEAR,
        jpy_charge: float = 0.0,
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

SINGLE_YEAR_TESTS = []
MULTI_YEAR_TESTS = []


def add_single_year_test(name: str, history: History, expected: float) -> None:
    SINGLE_YEAR_TESTS.append((name, history, {DEFAULT_YEAR: expected}))


add_single_year_test(
    "single_year",
    [
        Transaction("buy", 1, 100),
        Transaction("sell", 1, 200),
    ],
    100,
)
add_single_year_test(
    "single_year_negative",
    [
        Transaction("buy", 1, 200),
        Transaction("sell", 1, 100),
    ],
    -100,
)
add_single_year_test(
    "single_year_charge",
    [
        Transaction("buy", 1, 100),
        Transaction("sell", 0.5, 200, jpy_charge=10),
    ],
    140,
)
add_single_year_test(
    "single_year_multiple_sell",
    [
        Transaction("buy", 1, 100),
        Transaction("sell", 0.1, 20),
        Transaction("sell", 0.2, 50),
    ],
    40,
)
add_single_year_test(
    "single_year_multiple_buy",
    [
        Transaction("buy", 1, 100),
        Transaction("buy", 2, 170),
        Transaction("sell", 0.5, 200),
    ],
    155,
)
add_single_year_test(
    "single_year_multiple_buy_sell",
    [
        Transaction("buy", 1, 100),
        Transaction("buy", 2, 170),
        Transaction("buy", 3, 210),
        Transaction("sell", 1, 120),
        Transaction("sell", 1.5, 200),
    ],
    120,
)


def add_multi_year_test(
    name: str, year_history: Dict[int, History], expected: Dict[int, float]
) -> None:
    all_history = []
    for year, history in year_history.items():
        for transaction in history:
            transaction.year = year
            all_history.append(transaction)
    MULTI_YEAR_TESTS.append((name, all_history, expected))


add_multi_year_test(
    "two_year",
    {
        2020: [
            Transaction("buy", 10, 1000),
            Transaction("sell", 1, 150),
        ],
        2021: [
            Transaction("sell", 1, 200),
        ],
    },
    {
        2020: 50,
        2021: 100,
    },
)

add_multi_year_test(
    "two_year_buy",
    {
        2020: [
            Transaction("buy", 1, 100),
            Transaction("buy", 1, 120),
            Transaction("buy", 1, 140),
            Transaction("buy", 1, 160),
        ],
        2021: [
            Transaction("buy", 1, 80),
            Transaction("sell", 2, 200),
        ],
    },
    {
        2020: 0,
        2021: -40,
    },
)

add_multi_year_test(
    "two_year_buy_sell",
    {
        2020: [
            Transaction("buy", 1, 100),
            Transaction("buy", 1, 120),
            Transaction("buy", 1, 140),
            Transaction("buy", 1, 160),
            Transaction("sell", 3, 600),
        ],
        2021: [
            # Transferred from 2020: ("buy", 1, 130)
            Transaction("buy", 1, 80),
            Transaction("sell", 2, 200),
        ],
    },
    {
        2020: 210,
        2021: -10,
    },
)

add_multi_year_test(
    "two_year_buy_sell_charge",
    {
        2020: [
            Transaction("buy", 1, 100, jpy_charge=10),
            Transaction("buy", 1, 120, jpy_charge=12),
            Transaction("buy", 1, 140, jpy_charge=14),
            Transaction("buy", 1, 160),
            Transaction("sell", 3, 600, jpy_charge=50),
        ],
        2021: [
            Transaction("buy", 1, 80, jpy_charge=10),
            Transaction("sell", 2, 200, jpy_charge=20),
        ],
    },
    {
        2020: 124,
        2021: -40,
    },
)

add_multi_year_test(
    "three_year_buy",
    {
        2019: [
            Transaction("buy", 1, 100),
            Transaction("buy", 1, 120),
        ],
        2020: [
            Transaction("buy", 1, 140),
            Transaction("buy", 1, 160),
        ],
        2021: [
            Transaction("buy", 1, 180),
            Transaction("buy", 1, 200),
            Transaction("sell", 1, 200),
        ],
    },
    {
        2019: 0,
        2020: 0,
        2021: 50,
    },
)

add_multi_year_test(
    "three_year_buy_sell",
    {
        2019: [
            Transaction("buy", 1, 100),
            Transaction("buy", 1, 120),
            Transaction("sell", 1, 120),
        ],
        2020: [
            # Transferred from 2019: ("buy", 1, 110)
            Transaction("buy", 1, 150),
            Transaction("buy", 1, 160),
            Transaction("sell", 1, 130),
        ],
        2021: [
            # Transferred from 2020: {"buy", 2, 280}
            Transaction("buy", 1, 180),
            Transaction("buy", 1, 200),
            Transaction("sell", 1, 200),
        ],
    },
    {
        2019: 10,
        2020: -10,
        2021: 35,
    },
)

add_multi_year_test(
    "skip",
    {
        2017: [
            Transaction("buy", 1, 100),
            Transaction("buy", 1, 120),
            Transaction("sell", 1, 120),
        ],
        2019: [
            Transaction("buy", 1, 150),
            Transaction("buy", 1, 160),
            Transaction("sell", 1, 130),
        ],
        2021: [
            Transaction("buy", 1, 180),
            Transaction("buy", 1, 200),
            Transaction("sell", 1, 200),
        ],
    },
    {
        2017: 10,
        2018: 0,
        2019: -10,
        2020: 0,
        2021: 35,
    },
)

add_multi_year_test(
    "bubble_no_transaction",
    {
        2017: [
            Transaction("buy", 10, 100),
            Transaction("sell", 5, 500),
        ],
        # 2018: [
        #     Transaction("sell", 5, 10),
        #     Transaction("buy", 5, 10),
        # ],
        2021: [Transaction("sell", 5, 1000)],
    },
    {
        2017: 450,
        2018: 0,
        2019: 0,
        2020: 0,
        2021: 950,
    },
)

add_multi_year_test(
    "bubble_has_transaction",
    {
        2017: [
            Transaction("buy", 10, 100),
            Transaction("sell", 5, 500),
        ],
        2018: [
            Transaction("sell", 5, 10),
            Transaction("buy", 5, 10),
        ],
        2021: [Transaction("sell", 5, 1000)],
    },
    {
        2017: 450,
        2018: -20,
        2019: 0,
        2020: 0,
        2021: 970,
    },
)

ALL_TESTS = SINGLE_YEAR_TESTS + MULTI_YEAR_TESTS


@pytest.mark.parametrize(("name", "history", "expected"), ALL_TESTS)
def test_periodic_averaged(name: str, history: History, expected: Dict[int, float]) -> None:
    manager = PeriodicAveragedSingle("test")
    for transaction in history:
        transaction.register_to(manager)
    profits = manager.get_profits()
    assert profits == expected, name
