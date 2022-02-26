# crypto-kakutei
総平均法に基づく暗号通貨の確定申告用スクリプトです。**以下の注意事項をよくお読みになってからご利用ください。**

# 注意事項
* このレポジトリに含まれるプログラムの開発者およびコントリビュータは、不正確な確定申告による税務上のトラブル、もしくは本プログラムが招いたいかなる損害についても責任を追うことはありませんを負いません。
* 必ずご自身の責任のもとに計算結果を確認してください。
* とくに、暗号資産に関する税務上の取り扱いは年々変化しておりますので必ず国税庁のホームページにて最新の情報をご確認ください。令和3年度版は[こちら](https://www.nta.go.jp/publication/pamph/shotoku/kakuteishinkokukankei/kasoutuka/)。

# 使い方
## CSVファイルから読み込む場合
bitbank, coincheckのフォーマットに対応しています。
```python
from crykak.periodic_averaged import PeriodicAveraged
from crykak.csv_reader import register_from_csv

manager = PeriodicAveraged()
register_from_csv(manager, "2019.csv")
register_from_csv(manager, "2020.csv")
register_from_csv(manager, "2021.csv")

print(manager.get_total_profits())
```
総平均法の損益計算には、目的の年度だけではなく過去すべての取引履歴が必要です。

## 自分でデータを登録する場合
```python
from crykak.periodic_averaged import PeriodicAveraged

manager = PeriodicAveraged()
# 2017年に 200.0 jpy/xrp で 500 xrp 購入 (100000円)
manager.register_buy("xrp", 2017, 200.0, 500)
# 2017年に 250.0 jpy/xrp で 100 xrp 売却 (25000円)
manager.register_sell("xrp", 2017, 250.0, 100)

print(manager.get_total_profits())  # {2017: 5000.0}
```

`PeriodicAveraged`クラスがサポートする関数に関してはお手数ですが[crykak/periodic_averaged.py](https://github.com/xuzijian629/crypto-kakutei/blob/main/crykak/periodic_averaged.py)を御覧ください。

# 暗号通貨の確定申告における注意事項
暗号通貨の確定申告において知っておくべきことを[LEGAL.md](LEGAL.md)にまとめましたので、必要に応じて御覧ください。

# コントリビュータを募集しています
crypto-kakuteiではプログラムのバグの報告や、税務的な指摘、その他あらゆるフィードバックを歓迎しています。詳しくは[CONTRIBUTING.md](CONTRIBUTING.md)を御覧ください。