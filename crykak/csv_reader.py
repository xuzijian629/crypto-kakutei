import csv
from typing import Dict, Optional, Tuple

from crykak.periodic_averaged import PeriodicAveraged


def parse_bitbank_csv_line(line: Dict[str, str]) -> Tuple[str, str, int, float, float, float]:
    currency = line["通貨ペア"].split("_")[0]
    buy_or_sell = line["売/買"]
    year = int(line["取引日時"].split("/")[0])
    rate = float(line["価格"])
    amount = float(line["数量"])
    charge = float(line["手数料"])
    return currency, buy_or_sell, year, rate, amount, charge


def parse_coincheck_csv_line(
    line: Dict[str, str]
) -> Optional[Tuple[str, str, int, float, float, float]]:
    operation = line["operation"]
    assert operation in [
        "Buy",
        "Credit Card Purchase",
        "Sell",
        "Completed trading contracts",
        "Limit Order",
        "Cancel Limit Order",
        "Transfer",
        "Sent",
        "Received",
        "Bank Withdrawal",
    ], f"Unknown operation: {operation}"

    year = int(line["time"].split("-")[0])
    amount = float(line["amount"])
    currency = line["trading_currency"].lower()
    original_currency = line["original_currency"].lower()
    comment = line["comment"]
    if operation in ["Buy", "Credit Card Purchase"]:
        price = float(line["price"])
        assert amount > 0 and price < 0 and original_currency == "jpy"
        price = abs(price)
        return currency, "buy", year, price / amount, amount, 0
    elif operation == "Sell":
        price = float(line["price"])
        assert amount < 0 and price > 0 and original_currency == "jpy"
        amount = abs(amount)
        return currency, "sell", year, price / amount, amount, 0
    elif operation == "Completed trading contracts":
        assert "Rate: " in comment and "Pair: " in comment
        crypto, jpy = comment.split("Pair: ")[1].split("_")
        assert jpy == "jpy"
        rate = float(comment.split("Rate: ")[1].split(",")[0])
        if currency == crypto:
            return crypto, "sell", year, rate, amount, 0
        else:
            assert currency == "jpy"
            assert rate > 0
            return crypto, "buy", year, rate, amount / rate, 0
    else:
        return None


def register_from_csv(manager: PeriodicAveraged, csv_file: str) -> None:
    with open(csv_file, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        fields = reader.fieldnames
        if fields == "注文ID,取引ID,通貨ペア,タイプ,売/買,数量,価格,手数料,M/T,取引日時".split(","):
            csv_type = "bitbank"
        elif (
            fields
            == "id,time,operation,amount,trading_currency,price,original_currency,fee,comment".split(
                ","
            )
        ):
            csv_type = "coincheck"
        else:
            raise RuntimeError(
                f"Cannot parse csv with fields: {fields}. "
                "Currently, we only support csv files obtained from bitbank or coincheck."
            )

        for line in reader:
            parse_func = (
                parse_bitbank_csv_line if csv_type == "bitbank" else parse_coincheck_csv_line
            )
            parsed = parse_func(line)
            if parsed is None:
                continue
            currency, buy_or_sell, year, rate, amount, charge = parsed

            if buy_or_sell == "buy":
                manager.register_buy(currency, year, rate, amount, charge)
            elif buy_or_sell == "sell":
                manager.register_sell(currency, year, rate, amount, charge)
            else:
                raise ValueError(f"Unknown transaction kind: {buy_or_sell}.")
