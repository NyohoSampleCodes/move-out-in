# 04. 関数の定義

## 今回学ぶこと

- 関数とは何か、なぜ使うのか
- `def` で関数を定義する
- 引数（関数に渡す値）と `return`（関数から返す値）

## 関数とは

「転入者数から転出者数を引いて、転入超過数を求める」という計算を、いろいろな都道府県・いろいろな年で何度も行うことになります。そのたびに同じ計算を書き写すのは面倒ですし、書き間違いの元にもなります。

こういう「何度も使う処理」に名前をつけてまとめておいたものが **関数** です。

## def で定義する

```python
def calc_net(in_count, out_count):
    net = in_count - out_count
    return net
```

- `def 関数名(引数, ...):` で関数を作り始めます。
- `in_count`、`out_count` は **引数** です。関数を呼び出すときにここに値が渡されます。
- `return` は「この値を関数の結果として返す」という意味です。

## 呼び出してみる

```python
result = calc_net(53281, 59566)
print(result)  # -6285
```

`calc_net(53281, 59566)` のように書くと、`in_count` に `53281`、`out_count` に `59566` が渡されて関数の中の処理が実行され、`return net` の `net` の値が `result` に入ります。

同じ関数を、違う数値で何度でも呼び出せるのが便利なところです。

```python
print(calc_net(100, 80))   # 20
print(calc_net(30, 45))    # -15
```

## リストと組み合わせる

`03` で学んだ `for` 文と組み合わせると、複数の都道府県の計算をまとめて行えます。

```python
def calc_net(in_count, out_count):
    return in_count - out_count

in_counts = [53281, 21497]
out_counts = [59566, 22697]

for i in range(len(in_counts)):
    net = calc_net(in_counts[i], out_counts[i])
    print(net)
```

`range(len(in_counts))` は `0, 1, 2, ...` という数値を、リストの長さの分だけ順番に作ってくれます。これを使うと、2 つのリスト（`in_counts` と `out_counts`）の同じ位置（インデックス）の値を両方使って計算できます。

## 実際に動かしてみる

```
python steps/04_functions.py
```

## 演習

1. 「転入者数・転出者数を受け取って、`"転入超過"` か `"転出超過"` の文字列を返す」関数を作ってみましょう（ヒント: `if net >= 0:` のように条件分岐が使えます）。
2. `calc_net` を使って、3 つ以上の都道府県分の転入超過数を `for` 文でまとめて表示してみましょう。

次は [05. ファイルの読み書き](05_file_io.md) に進んでください。
