crypto-kakuteiに興味をもっていただき、ありがとうございます。
このページでは、バグの報告やコードの修正をする上での手順を紹介します。

# バグ報告、フィードバックについて
[Issuesタブ](https://github.com/xuzijian629/crypto-kakutei/issues)から[New issue](https://github.com/xuzijian629/crypto-kakutei/issues/new/choose)を選んでissueの作成をお願いします。

* プログラムのバグの場合、バグを再現する手順を添えていただけると助かります。
* 税務的な指摘（たとえば[LEGAL.md](LEGAL.md)の内容の間違い）の場合は、正しい情報とそのソースを載せていただけると助かります。

# プルリクエストについて
ご自身でプルリクエストを作成できる場合には作成していただけると大変助かります。
アルゴリズムについての変更の場合、その正当性を確認できるテストを追加していただきたく思っております。

## 環境構築
```bash
pip install -r pysen-requirements.txt
pip install -e ".[test]"
```

## テスト追加方法
テストは`tests/`以下にあり、pytestを使ってテストしております。
正しい損益の計算方法としては、
[国税庁](https://www.nta.go.jp/publication/pamph/shotoku/kakuteishinkokukankei/kasoutuka/)から移動平均法および総平均法に基づく損益計算ができるExcelファイルが配布されていますので、ご活用ください。

## テストの実行
`pysen run lint`でpythonのスタイルチェックを行っています。
`pysen run format`で一部のlintエラーを修正できます。

```bash
pysen run lint
pytest
```