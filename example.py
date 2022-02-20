from periodic_averaged import PeriodicAveraged


if __name__ == "__main__":
    manager = PeriodicAveraged("xrp")
    # 2017年に 200.0 jpy/xrp で 500 xrp 購入 (100000円)
    manager.register_buy(2017, 200.0, 500)
    # 2017年に 250.0 jpy/xrp で 100 xrp 売却 (25000円)
    manager.register_sell(2017, 250.0, 100)

    manager.register_sell(2021, 80.0, 300)
    manager.register_buy(2021, 60.0, 50)

    print(manager.get_profits())