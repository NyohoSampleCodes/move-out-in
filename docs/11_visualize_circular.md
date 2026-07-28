# 11. 円環レイアウトと hover 連動

いよいよ [vis_peopleflow](https://klareswasser.github.io/vis_peopleflow/) の見た目に近づけます。47都道府県を円周上に並べ、外周のバーで転入超過・転出超過を、都道府県にマウスを乗せたときにその県の転入・転出の流れを表示する図を作ります。

**この回は今までより少し難しくなります。** 三角関数を使った座標計算、曲線の描き方、そして新しく `Dash` というライブラリを使います。わからない部分は読み飛ばして、まず動かしてみるのでも構いません。

## 今回学ぶこと

- 三角関数（`math.cos`, `math.sin`）で、円周上に等間隔に点を並べる
- ベジェ曲線で、都道府県同士を結ぶ「弧」を描く
- `Dash` で、hover（マウスを乗せる操作）をきっかけに図を描き直す

## なぜ plotly だけでは足りないのか

`10` で作ったサンキー図は、`fig.write_html(...)` で1枚の HTML ファイルを作れば完成でした。しかし今回作りたいのは、「都道府県 A にマウスを乗せたら、そのときだけ A の出入りの線を表示する」という**操作に応じて図が変わる**ものです。これは、あらかじめ1枚の絵を描いておくだけでは実現できません。

そこで `Dash` というライブラリを使います。Dash は、自分のパソコンの中に小さな Web サーバーを立ち上げて、

1. ブラウザで都道府県にマウスを乗せる（hover）
2. その情報がサーバー側の Python に送られる
3. `04` で学んだ「関数」が呼ばれて、新しい図を計算する
4. 計算された図がブラウザに送り返され、画面が更新される

という流れを裏側でやってくれます。難しく感じるかもしれませんが、実は「hover されたら、こちらで用意しておいた関数が自動的に呼ばれる」という点は、これまで自分で `calc_net(...)` のように関数を呼び出していたのと同じ仕組みです。呼び出すきっかけが「自分でコードを書く」から「ブラウザでの操作」に変わっただけです。

`Dash` はすでに `uv add dash` で追加してあります。

## 弧だけでは「どちらへの流れか」が伝わらない

まず、`08` の `flows`（`[転出元, 転入先, 人数]` のリスト）を使って、hover した都道府県の転出・転入を弧で描いてみます。転出＝青、転入＝赤で色分けし、移動者数が多いほど太くします。

ところが、これを実際に試してみると、大きな問題に気づきます。**1本の弧は、都道府県 A と都道府県 B を結んでいるだけで、太さも色も両端でまったく同じです。** 赤い弧を見て「転入だ」とわかっても、その弧の A 側の端と B 側の端は見た目がまったく区別できないので、「A に入ってきているのか、B に入ってきているのか」は弧そのものからはわかりません。

矢印を弧に添える、根元を太く先端を細くするテーパー処理にする、弧の上を点が動くアニメーションにする、といったやり方もいろいろ試しました。しかし47都道府県ぶんの弧が重なり合うとかえって見づらくなったり、`Dash` はサーバーとブラウザを1往復させて図を作り直す都合上、アニメーションにするとカクついてしまったりと、うまくいきませんでした。

最終的にたどり着いたのが、この節のタイトルにもある**半透明の重なり**です。動きに頼らず、静止した図だけで「今 hover している都道府県に向かって、あるいはそこから、弧が集まっている」ことが伝わる表現になります。

## 円周上に都道府県を並べる

47都道府県を円周上に均等に並べるには、それぞれの都道府県に「角度」を割り当てて、その角度から `x, y` 座標を計算します。円周上の点は、中心からの角度 `angle` と半径 `radius` を使って次の式で求められます（`math.cos`・`math.sin` は三角関数で、`math` モジュールに入っています）。

```python
import math

def polar_to_xy(index, radius, total):
    angle = 2 * math.pi * index / total - math.pi / 2
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y
```

- `2 * math.pi` は円1周分の角度（ラジアンという単位での360度）です。`index / total` で「47個中の何番目か」を0〜1の割合にし、それに1周分をかけることで、47都道府県に均等な角度を割り振っています。
- 最後に `- math.pi / 2` しているのは、0番目（北海道）が真上（12時の方向）から始まるように、開始位置をずらしているだけです。

これで `index=0`（北海道）は円の上のほう、`index=23`（三重県、47の半分あたり）は下のほう、というふうに、都道府県コードの順番のまま時計回りに配置されます。

## 外周のバー（転入超過・転出超過）

`09` の棒グラフと同じ考え方で、`net`（転入超過数）の絶対値の大きさだけ、円の少し外側に向かって線を伸ばします。

```python
inner_x, inner_y = polar_to_xy(i, 1.0, 47)
outer_x, outer_y = polar_to_xy(i, 1.0 + abs(net[i]) * bar_scale, 47)
```

半径 `1.0` の位置から、`net[i]` の絶対値に応じてもう少し外側の位置まで、線を1本引きます。転入超過なら赤、転出超過なら青にします（`09` の色分けと同じ考え方です）。

## ベジェ曲線で弧を描く

2つの都道府県を直線で結ぶと、線がすべて円の中心を突っ切ってしまい、ごちゃごちゃした絵になります。vis_peopleflow のような弧を描くには、**ベジェ曲線**というカーブの描き方を使います。

2点を結ぶ滑らかな曲線を作るには、始点・終点に加えて「曲線がどちらに膨らむか」を決める**制御点**を1つ用意します。

```python
def bezier_points(p0, p1, control, n=30):
    xs = []
    ys = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * control[0] + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * control[1] + t ** 2 * p1[1]
        xs.append(x)
        ys.append(y)
    return xs, ys
```

この式の中身を完全に理解する必要はありません。「`t` を `0` から `1` まで少しずつ動かしながら、始点・制御点・終点の3つを混ぜ合わせた位置を `n+1` 個計算すると、なめらかな曲線になる」というのがベジェ曲線の考え方です。制御点をどこに置くかで、曲線の膨らみ方が変わります。

## ホバーされた都道府県の flows だけを描く

`08` で作った `flows` から、あらかじめ都道府県ごとに「関係する flows」を仕分けておきます。

```python
out_flows_by_pref = [[] for _ in range(47)]
in_flows_by_pref = [[] for _ in range(47)]
for from_index, to_index, count in flows:
    out_flows_by_pref[from_index].append((from_index, to_index, count))
    in_flows_by_pref[to_index].append((from_index, to_index, count))
```

これで「ある都道府県の番号」から、その県が関わる転出・転入の一覧をすぐに取り出せます。

## 移動者数に応じて線の太さを変える

すべての弧を同じ太さで描くと、「たくさん移動している相手」も「少ししか移動していない相手」も同じ見た目になってしまいます。移動者数（`count`）が多いほど太い線になるようにしましょう。

ここで1つ注意点があります。`plotly` の `Scatter` は、**1つの trace（線のかたまり）につき太さを1つしか指定できません**。`10` のサンキー図では県のペアの数だけ `flows` を扱いましたが、あのときは太さの指定は plotly 側にまかせていました。今回は自分で弧を描いているので、線ごとに太さを変えたいなら、**弧の数だけ trace を作る**必要があります。

```python
def flow_width(count, max_count):
    min_width = 0.8
    max_width = 4.0
    return min_width + (max_width - min_width) * (count / max_count)
```

`max_count`（その県の転出先の中で一番多い人数）を基準に、`count / max_count` で「その移動が相対的にどれくらい多いか」を 0〜1 の割合にし、`min_width`〜`max_width` の太さに変換しています。

## 転出と転入の弧が重なってしまう問題

色分け（転出＝青、転入＝赤）と太さだけで試してみると、1つ問題が出てきます。ある都道府県との間で転出も転入も多い場合（東京都と神奈川県の関係など）、2本の太い弧がほぼ同じ場所に重なって描かれ、**あとから描いた方の色で塗りつぶされて、もう片方が見えなくなってしまう** のです。

対策として、転出の弧と転入の弧を、ほんの少しだけ左右にずらして描きます。1本の道を2車線に分けるイメージです。

```python
def perpendicular_offset(base, target, amount):
    dx = target[0] - base[0]
    dy = target[1] - base[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return (0, 0)
    return (-dy / length * amount, dx / length * amount)
```

`(dx, dy)` は「hover 中の都道府県（`base`）から相手（`target`）への向き」を表すベクトルです。`(-dy, dx)` は、そのベクトルを90度回転させた「進行方向に対して垂直な向き」になります。この垂直な向きに `amount` の分だけ動かした位置を、ベジェ曲線の制御点として使います。

```python
self_pos = polar_to_xy(pref_index, 1.0, 47)

# 転出：hover 中の都道府県 → 相手 の向きから、垂直に +offset
other_pos = polar_to_xy(to_index, 1.0, 47)
offset = perpendicular_offset(self_pos, other_pos, 0.15)
xs, ys = bezier_points(self_pos, other_pos, control=offset)

# 転入：同じ基準（hover 中の都道府県 → 相手）で、符号だけ逆にする
other_pos = polar_to_xy(from_index, 1.0, 47)
offset = perpendicular_offset(self_pos, other_pos, -0.15)
xs, ys = bezier_points(other_pos, self_pos, control=offset)
```

ポイントは、**転出でも転入でも、常に「hover 中の都道府県から相手への向き」を基準にオフセットを計算していること** です。転入の弧は始点と終点が転出とは逆（相手 → 自分）になるので、もし「線の始点から終点への向き」を基準にしてしまうと、符号を反転させても実際には同じ側にずれてしまいます（試して確認しました）。基準を hover 中の都道府県に統一することで、転出は常に片側、転入は常に反対側にきれいに分かれます。

## 半透明にして、重なりで濃淡をつける

47都道府県ぶんの弧を描くと、hover した都道府県のまわりには多くの弧が集まり、遠くの相手県に向かうにつれて1本だけになっていきます。ここで弧を**半透明**にしておくと、面白いことが起きます。**重なっている場所ほど、色が自然に濃くなる** のです。

```python
traces.append(go.Scatter(
    x=xs, y=ys, mode="lines",
    line=dict(color="royalblue", width=flow_width(count, max_out)),
    opacity=0.35, hoverinfo="skip",
    ...
))
```

`opacity=0.35` のように 1 より小さい値を指定するだけです。これだけで、hover した都道府県の近くでは大量の弧が同じような場所を通るために色が濃くなり、相手県に近づくにつれて弧はばらばらの方向へ散っていくので色が薄くなります。**「濃い方が今 hover している都道府県、薄い方が相手県」** という手がかりが、色を覚えていなくても伝わるようになります。

## 色の意味を凡例で示す

47都道府県ぶんの弧をそれぞれ別の trace として作っているため、何も工夫しないと凡例に「転出」が92個も並んでしまいます。同じ意味を持つ trace を `legendgroup` でグループにまとめ、グループの中で最初の1本だけ `showlegend=True` にすることで、凡例には「転出」「転入」の2項目だけを表示できます。

```python
for i, (from_index, to_index, count) in enumerate(out_flows):
    ...
    traces.append(go.Scatter(
        ...,
        legendgroup="out", name="転出", showlegend=(i == 0),
    ))
```

`showlegend=(i == 0)` は、「`i` が `0`（そのグループの最初の要素）のときだけ `True`」という意味です。

## Dash アプリを組み立てる

Dash アプリは、「画面に何を表示するか」（`layout`）と、「何かが起きたら何をするか」（`callback`）の2つでできています。

```python
from dash import Dash, Input, Output, dcc, html

app = Dash(__name__)

app.layout = html.Div([
    html.H3("都道府県間の人口移動（円環配置）"),
    dcc.Graph(id="chord-graph", figure=build_figure()),
])


@app.callback(
    Output("chord-graph", "figure"),
    Input("chord-graph", "hoverData"),
)
def on_hover(hover_data):
    if hover_data is None:
        return build_figure(None)

    point = hover_data["points"][0]
    if point.get("curveNumber") != 0:
        # 都道府県のノード以外（外周バーなど）は無視する
        return build_figure(None)

    pref_index = point["pointIndex"]
    return build_figure(pref_index)


if __name__ == "__main__":
    app.run(debug=False)
```

- `dcc.Graph(id="chord-graph", ...)` が、plotly の図を表示する部品です。`id` をつけておくと、あとで `callback` からこの部品を指定できます。
- `@app.callback(Output("chord-graph", "figure"), Input("chord-graph", "hoverData"))` は「`chord-graph` の `hoverData`（マウスを乗せた場所の情報）が変化したら、この関数を実行して、その結果を `chord-graph` の `figure`（表示する図）に反映する」という意味です。
- `hover_data["points"][0]` に、マウスを乗せた場所の情報が入っています。`pointIndex` が、`polar_to_xy` で並べたときの都道府県の番号（`prefs` のインデックス）と一致するように作ってあるので、そのまま `build_figure` に渡せます。
- 外周バーのトレース（線）にマウスが乗ったときは何もしたくないので、`curveNumber`（何番目の trace か）で判定して、都道府県のノード（0番目の trace）のときだけ処理しています。

`build_figure(pref_index)` は、`pref_index` が `None` なら都道府県のノードと外周バーだけを、番号が指定されていればそれに加えて転入・転出の弧（半透明・凡例つき）を含んだ `plotly` の `Figure` を組み立てて返す関数です。詳しくは `steps/11_visualize_circular.py` を読んでみてください。

## 実際に動かしてみる

これまでとは実行方法が少し違います。ファイルが1つできて終わり、ではなく、**サーバーが起動し続けます**。

```
python steps/11_visualize_circular.py
```

実行すると、ターミナルに次のように表示されます。

```
Dash is running on http://127.0.0.1:8050/
```

この `http://127.0.0.1:8050/` を、ブラウザのアドレス欄に入力して開いてください。都道府県の点にマウスを乗せると、左上の凡例（青＝転出、赤＝転入）とあわせて、その県の転出・転入の弧が表示されます。その県のまわりでは弧が重なって色が濃く、遠い相手県に近づくほど薄くなっているはずです。

終了するときは、ターミナルに戻って `Ctrl + C` を押してください。サーバーが停止します。

## 演習

1. `FLOW_OPACITY` の値を変えて、重なりによる濃淡の出方がどう変わるか試してみましょう。
2. `ARC_OFFSET`（`0.15`）の値を変えて、転出と転入の弧がどれくらい離れるとわかりやすいか試してみましょう。
3. `flow_width` の `min_width` と `max_width` の値を変えて、線の太さのメリハリがどう変わるか試してみましょう。
4. `Input("chord-graph", "hoverData")` を `Input("chord-graph", "clickData")` に変えると、hover ではなくクリックで反応するようになります。試してみて、どちらが使いやすいか考えてみましょう。

次は [12. 複数年のデータをまとめて扱う](12_multi_year.md) に進んでください。
