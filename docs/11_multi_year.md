# 11. 複数年のデータをまとめて扱う

## 今回学ぶこと

- 同じ処理を、年を変えながら関数として繰り返す
- ファイルが存在するかどうかを確認する（`pathlib`）
- 複数年をまとめた JSON と、推移の折れ線グラフ

## これまでの復習

`08` で作った「Excel を読んで、47×47の行列にする」処理と、「行列から転入超過数を計算する」処理は、どちらも `04` で学んだ関数として書かれていました。関数にしておいたおかげで、**年が変わっても同じコードをそのまま使い回せます。**

```python
def load_matrix(file_path):
    ...  # 08 と同じ

def calc_net(matrix):
    ...  # in_totals, out_totals から net を計算する部分だけを取り出したもの
```

## ファイルがあるかどうかを確認する

06 で用意したデータは 2020・2021・2022・2024 年の4年分で、2023年は含まれていません。存在しないファイルを `load_matrix` に渡すとエラーになってしまうので、先に `pathlib` というライブラリでファイルの存在を確認します。

```python
from pathlib import Path

file_path = Path("data/raw/idou_2023.xlsx")
if file_path.exists():
    print("ファイルがあります")
else:
    print("ファイルがありません")
```

`Path(...)` はファイルパスを扱いやすくする道具で、`.exists()` で「そのパスに実際にファイルがあるか」を `True` / `False` で教えてくれます。

## 年ごとにループして処理する

```python
years = [2020, 2021, 2022, 2023, 2024]

net_by_year = {}
for year in years:
    file_path = Path(f"data/raw/idou_{year}.xlsx")
    if not file_path.exists():
        print(year, "年のファイルが見つからないのでスキップします")
        continue

    matrix = load_matrix(file_path)
    net = calc_net(matrix)
    net_by_year[year] = net
    print(year, "年を処理しました")
```

- `f"data/raw/idou_{year}.xlsx"` は「f文字列」という書き方で、`{year}` の部分が変数の値に置き換わります。`year` が `2020` なら `"data/raw/idou_2020.xlsx"` になります。
- `continue` は「これ以降の処理をとばして、`for` の次のループに進む」という意味です。ファイルがない年はここでスキップされます。
- `net_by_year` は「年をキー、47都道府県ぶんの `net` リストを値とする辞書」です。2023年のようにファイルがない年は含まれません。

## まとめて JSON に保存する

```python
import json

output = {
    "prefs": PREFECTURES,
    "years": {str(year): net for year, net in net_by_year.items()},
}

with open("data/processed/migration_all.json", "w", encoding="utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=2)
```

`net_by_year.items()` は、辞書の中身を `(キー, 値)` の組として順番に取り出します。JSON の中ではキーは必ず文字列である必要があるため、`str(year)` で `2020` を `"2020"` に変換しています。vis_peopleflow の `migration_data.json` にも `years` というキーで年ごとのデータがまとまっていたのを思い出してください。今回作ったデータも同じような構造になっています。

## 推移を折れ線グラフにする

特定の都道府県について、年ごとの転入超過数がどう変わってきたかを見てみましょう。

```python
import matplotlib.pyplot as plt
import japanize_matplotlib

tokyo_index = PREFECTURES.index("東京都")

years_list = sorted(net_by_year.keys())
tokyo_net = [net_by_year[year][tokyo_index] for year in years_list]

plt.plot(years_list, tokyo_net, marker="o")
plt.ylabel("転入超過数（人）")
plt.title("東京都の転入超過数の推移")
plt.savefig("data/processed/trend.png")
```

- `PREFECTURES.index("東京都")` は、リストの中から `"東京都"` が何番目にあるかを教えてくれます。
- `plt.plot(x軸のリスト, y軸のリスト, marker="o")` で折れ線グラフを描きます。`marker="o"` は各点に丸印をつける指定です。

## 実際に動かしてみる

```
uv run python steps/11_multi_year.py
```

`data/processed/migration_all.json` と `data/processed/trend.png` ができます。2023年のファイルがない状態なので、実行中に「2023 年のファイルが見つからないのでスキップします」と表示されるはずです。

## 演習

1. 06 の発展課題で 2023年のデータをダウンロードして `data/raw/idou_2023.xlsx` として保存し、もう一度実行してみましょう。スキップされずに処理されるはずです。
2. `"東京都"` を別の都道府県名に変えて、その県の推移を見てみましょう。地方の県と都市部の県で、折れ線の形がどう違うか比べてみてください。

次は [12. まとめと次の一歩](12_next_steps.md) に進んでください。
