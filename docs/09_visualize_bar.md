# 09. matplotlib で棒グラフ

## 今回学ぶこと

- `matplotlib` の基本的な使い方
- 08 で作った JSON を読み込んでグラフにする
- 日本語ラベルを文字化けさせずに表示する

## matplotlib とは

`matplotlib` は Python で最もよく使われるグラフ描画ライブラリです。すでに `uv add matplotlib` で追加してあります。

## JSON を読み込む

08 で保存した `migration_2024.json` を、`json` モジュールで読み込みます。書き込みが `json.dump`、読み込みは `json.load` です。

```python
import json

with open("data/processed/migration_2024.json", encoding="utf-8") as file:
    data = json.load(file)

prefs = data["prefs"]
net = data["net"]
```

辞書に `["prefs"]` のようにキーを指定すると、保存しておいたリストがそのまま取り出せます。

## 日本語が文字化けする問題

matplotlib は標準では日本語のフォントを持っていないため、都道府県名をそのままグラフに使うと `□□□` のような文字化けになってしまうことがあります。これを避けるために `japanize-matplotlib` というライブラリを使います（これも `uv add japanize-matplotlib` で追加済みです）。

```python
import matplotlib.pyplot as plt
import japanize_matplotlib  # import するだけで日本語フォントの設定が有効になる
```

## 棒グラフを描く

```python
plt.figure(figsize=(14, 6))
plt.bar(prefs, net)
plt.xticks(rotation=90)
plt.ylabel("転入超過数（人）")
plt.title("都道府県別 転入超過数 (2024年)")
plt.tight_layout()
```

- `plt.figure(figsize=(14, 6))` で図の大きさ（横14インチ、縦6インチ）を指定します。47都道府県分のラベルを並べるので、横に広めにとっています。
- `plt.bar(x軸のリスト, 高さのリスト)` が棒グラフ本体です。
- `plt.xticks(rotation=90)` で、横軸のラベル（都道府県名）を90度回転させ、重ならないようにしています。
- `plt.tight_layout()` は、はみ出したラベルなどをいい感じに収める調整です。

転入超過（プラス）か転出超過（マイナス）かで色を変えると、ひと目でわかりやすくなります。`03` の `for` 文を使って、都道府県ごとに色のリストを作ります。

```python
colors = []
for value in net:
    if value >= 0:
        colors.append("tab:red")
    else:
        colors.append("tab:blue")

plt.bar(prefs, net, color=colors)
```

## 保存して確認する

```python
plt.savefig("data/processed/net_2024.png")
```

画面が使える環境では `plt.show()` でウィンドウにグラフを表示することもできますが、このプロジェクトでは `savefig` でファイルに保存する方法を使います。

## 実際に動かしてみる

```
uv run python steps/09_visualize_bar.py
```

`data/processed/net_2024.png` が作られます。開いてみると、東京都・神奈川県・埼玉県・千葉県・大阪府あたりが大きく赤（転入超過）に、多くの県が青（転出超過）になっているはずです。08 の演習で目で探した最大・最小の都道府県と一致しているか確認してみましょう。

## 演習

1. `net` の代わりに `data["in"]`（転入者数そのもの）や `data["out"]`（転出者数そのもの）を棒グラフにしてみましょう。
2. `08` の関数を使って、他の年（例: `idou_2020.xlsx`）の JSON を作り、同じグラフを描いて見た目を比べてみましょう。

次は [10. plotly でインタラクティブな図](10_visualize_interactive.md) に進んでください。
