# 10. plotly でインタラクティブな図

## 今回学ぶこと

- `plotly` で、マウスで触れる（ホバー・拡大縮小できる）図を作る
- 「サンキーダイアグラム」で、どの県からどの県へ人が流れているかを表現する
- `sorted()` でリストを並べ替える

## 09 の棒グラフでは足りないこと

09 の棒グラフは、都道府県ごとの「転入超過数」というひとつの数字は見せてくれますが、「具体的にどの県からどの県へ人が動いたか」は見せてくれません。vis_peopleflow の円環チャートが表現していたのは、まさにこの「県から県への流れ」でした。

`08` で作った `flows`（`[転出元, 転入先, 人数]` のリスト）を使えば、この「流れ」を可視化できます。今回は **サンキーダイアグラム** という、帯の太さで量を表す図を使います。

## plotly とは

`plotly` は、ブラウザで開ける HTML ファイルとしてグラフを出力できるライブラリです。マウスを乗せると数値が表示されたり、ドラッグで動かせたりする、インタラクティブな図が作れます（すでに `uv add plotly` で追加済みです）。

## flows を絞り込む

47都道府県 × 47都道府県ぶんの `flows` を全部表示すると、線が多すぎて何が何だかわからなくなってしまいます。そこで、人数の多い上位だけに絞り込みます。

```python
sorted_flows = sorted(flows, key=lambda flow: flow[2], reverse=True)
top_flows = sorted_flows[:30]
```

- `sorted(リスト, key=..., reverse=True)` は、リストを並べ替えます。`reverse=True` で大きい順（降順）になります。
- `key=lambda flow: flow[2]` は「並べ替えの基準として、各要素（`flow`）の3番目の値（`flow[2]`、つまり人数）を使う」という意味です。`lambda` は名前をつけない小さな関数だと思ってください。`04` で学んだ `def` を使わずに、その場限りの関数をさっと作る書き方です。
- `[:30]` は「先頭から30個だけ取り出す」というリストの切り出しです。

これで「移動者数が多い上位30ルート」だけが `top_flows` に入ります。

## サンキーダイアグラムを作る

```python
import plotly.graph_objects as go

sources = [flow[0] for flow in top_flows]
targets = [flow[1] for flow in top_flows]
values = [flow[2] for flow in top_flows]

fig = go.Figure(data=[go.Sankey(
    node=dict(label=prefs, pad=10, thickness=15),
    link=dict(source=sources, target=targets, value=values),
)])
fig.update_layout(title_text="都道府県間の人口移動 上位30 (2024年)", font_size=10)
```

- `[flow[0] for flow in top_flows]` は「リスト内包表記」という書き方で、`for` 文を1行で書けます。次と同じ意味です。

  ```python
  sources = []
  for flow in top_flows:
      sources.append(flow[0])
  ```

- `go.Sankey` の `node` には、図に表示するすべての都道府県名（`prefs`）を渡します。`link` の `source`・`target`・`value` には、それぞれ「流れの出発点」「流れの到着点」「量」のリストを渡します。都道府県名そのものではなく `08` で使った番号（インデックス）で指定する点に注意してください。

## HTML として保存する

```python
fig.write_html("data/processed/flows_2024.html")
```

`plt.savefig` が画像を保存したのに対して、plotly の図は `write_html` で HTML ファイルとして保存します。このファイルはブラウザでそのまま開けます。

## 実際に動かしてみる

```
python steps/10_visualize_interactive.py
```

`data/processed/flows_2024.html` ができるので、ブラウザで開いてみてください。帯にマウスを乗せると「〇〇県 → △△県: ×××人」のように表示され、ドラッグで都道府県のブロックを動かすこともできます。

## 演習

1. `top_flows = sorted_flows[:30]` の `30` を `10` や `100` に変えて、見やすさがどう変わるか確認してみましょう。
2. 特定の都道府県（例: 東京都）が関わる `flows` だけを `if flow[0] == 12 or flow[1] == 12:` のような条件で絞り込んで、その県だけの出入りを図にしてみましょう（東京都は `prefs` の12番目、インデックス12です）。

次は [11. 円環レイアウトと hover 連動](11_visualize_circular.md) に進んでください。
