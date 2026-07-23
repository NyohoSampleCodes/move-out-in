# 03. リストと for 文

## 今回学ぶこと

- リスト（複数の値をまとめて持っておく箱）
- `for` 文（リストの中身をひとつずつ処理する）
- `len()`、合計を求める

## リストとは

47 都道府県の名前をひとつひとつ別々の変数に入れていたら大変です。こういうときは「リスト」を使って、複数の値をひとつの変数にまとめます。

```python
prefectures = ["北海道", "青森県", "岩手県", "宮城県"]
print(prefectures)
```

リストは `[` と `]` で値を囲み、`,` で区切ります。

## 中身を1つ取り出す（インデックス）

リストの中の値には、先頭から数えた番号（インデックス）でアクセスできます。**最初の要素は 0 番目** です。

```python
print(prefectures[0])  # 北海道
print(prefectures[1])  # 青森県
```

## for 文でひとつずつ処理する

リストの中身をすべて順番に処理したいときは `for` 文を使います。

```python
for prefecture in prefectures:
    print(prefecture)
```

これは「`prefectures` の中身をひとつずつ取り出して `prefecture` という名前で使い、`print(prefecture)` を繰り返す」という意味です。実行すると `北海道`・`青森県`・`岩手県`・`宮城県` が順番に表示されます。

## len() と数値のリスト

リストに入っている個数は `len()` で調べられます。

```python
print(len(prefectures))  # 4
```

数値のリストを使えば、合計を計算することもできます。

```python
net_changes = [-8637, -3080, -3080, 500]

total = 0
for change in net_changes:
    total = total + change

print(total)
```

`total = total + change` は「今の `total` に `change` を足して、また `total` に入れなおす」という意味です。最初に `total = 0` としておくのを忘れないようにしましょう。

## 実際に動かしてみる

```
uv run python steps/03_lists_and_loops.py
```

`steps/03_lists_and_loops.py` には、47 都道府県すべてのリストが入っています。このリストは、これから先のステップでも何度も使う「共通の並び順」なので、ここで見た形を覚えておいてください（北海道から沖縄県まで、都道府県コードの順番です）。

## 演習

1. `net_changes` の数値を書き換えて、合計がどう変わるか確認してみましょう。
2. `for` 文の中で `print(prefecture, "の人口は減っています")` のように、リストの中身と文字列を組み合わせて表示してみましょう。

次は [04. 関数の定義](04_functions.md) に進んでください。
