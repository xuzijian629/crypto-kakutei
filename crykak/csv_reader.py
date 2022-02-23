import csv
from typing import Dict, Tuple

from crykak.periodic_averaged import PeriodicAveraged


def parse_bitbank_csv_line(line: Dict[str, str]) -> Tuple[str, str, int, float, float, float]:
    currency = line["通貨ペア"].split("_")[0]
    buy_or_sell = line["売/買"]
    year = int(line["取引日時"].split("/")[0])
    rate = float(line["価格"])
    amount = float(line["数量"])
    charge = float(line["手数料"])
    return currency, buy_or_sell, year, rate, amount, charge


def parse_coincheck_csv_line(line: Dict[str, str]) -> Tuple[str, str, int, float, float, float]:
    raise NotImplementedError()


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
            currency, buy_or_sell, year, rate, amount, charge = parse_func(line)

            if buy_or_sell == "buy":
                manager.register_buy(currency, year, rate, amount, charge)
            elif buy_or_sell == "sell":
                manager.register_sell(currency, year, rate, amount, charge)
            else:
                raise ValueError(f"Unknown transaction kind: {buy_or_sell}.")
