# 07. Excel を Python で読む

## 今回学ぶこと

- 標準の Python だけではできないことと、外部ライブラリ
- `openpyxl` で Excel ファイルを開く
- ワークブック・シート・セルという考え方
- 行番号・列番号でセルの値を取得する

## 外部ライブラリとは

これまで使ってきた `print()` や `open()` は、Python に最初から入っている機能でした。しかし Excel ファイル（`.xlsx`）は特殊な形式なので、それを読み書きするには専用の道具が必要です。こういう「あとから追加する道具」を **外部ライブラリ** と呼びます。

このプロジェクトでは、すでに次のコマンドで `openpyxl` というライブラリを追加してあります（`uv add` は `pip install` の uv 版です）。

```
uv add openpyxl
```

`pyproject.toml` を見ると、`openpyxl` が依存ライブラリとして書かれているはずです。自分の環境でも足りないライブラリがあれば `uv add ライブラリ名` で追加できます。

## ファイルを開く

```python
import openpyxl

workbook = openpyxl.load_workbook("data/raw/idou_2024.xlsx", data_only=True)
```

- `import openpyxl` で、そのライブラリを使えるようにします。
- `openpyxl.load_workbook(ファイルパス, data_only=True)` で Excel ファイル全体（**ワークブック**）を開きます。`data_only=True` は「数式ではなく、計算済みの値を読み込む」という指定です。

## シートを選ぶ

1つの Excel ファイルには、複数の「シート」（タブ）が含まれることがあります。今回のファイルには `a002` という名前のシートが1つだけ入っています。

```python
sheet = workbook["a002"]
```

## セルの値を読む

シートの中の1マス（セル）は、行番号と列番号で指定します。**Excel と同じく、1行目・1列目が最初です**（0番目からではありません。ここは `03` のリストのインデックスとは違うので注意）。

```python
value = sheet.cell(row=9, column=7).value
print(value)  # 北海道
```

これは Excel で言う「A9 セルから数えて7列目」、つまり9行7列目のセルの値です。06 で説明した通り、9行目からが都道府県のデータで、7列目に都道府県名（移動前の住所地）が入っています。

## この表の値の並び方

06 で見た構成をもう一度、セルの番地で表すとこうなります。

- 転出元（移動前の住所地）: **9〜55行目**、47都道府県が北海道から沖縄県の順に並ぶ
- 転入先（移動先）: **11列目から3列おき**（11, 14, 17, ...）に47都道府県分の「総数」列が並ぶ（あいだの列は男女別の内訳なので、今回は使わない）

つまり、「北海道からの転出データ」は9行目、「青森県への転入」は14列目なので、

```python
value = sheet.cell(row=9, column=14).value
print(value)  # 北海道から青森県への移動者数
```

自分の県から自分の県への移動にあたるセル（例: 北海道の行 × 北海道の列）は、06 で説明した通り `-` という文字列が入っています。

```python
value = sheet.cell(row=9, column=11).value
print(value)  # '-'
print(type(value))  # <class 'str'>
```

このあと集計するときは、この `-` を `0` として扱います。

## 47 × 47 のデータをまとめて読む

`03` の `for` 文と組み合わせれば、47都道府県 × 47都道府県、全部で 2209 マスのデータを読み込めます。

```python
for row_index in range(47):
    excel_row = 9 + row_index
    for col_index in range(47):
        excel_col = 11 + col_index * 3
        value = sheet.cell(row=excel_row, column=excel_col).value
        # ここで value を使って何かする
```

外側の `for` が転出元（行）、内側の `for` が転入先（列）を動かしています。`for` の中に `for` を書く「二重ループ」で、すべての組み合わせを1つずつ処理できます。

## 実際に動かしてみる

```
python steps/07_read_excel.py
```

## 演習

1. `row` や `column` の数値を変えて、他の都道府県同士の移動者数を表示してみましょう。
2. `-` になっているセルを見つけて、`if value == "-":` で判定し、`0` に置き換えて表示してみましょう。

次は [08. データを JSON にまとめる](08_build_json.md) に進んでください。
