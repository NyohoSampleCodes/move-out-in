# 08. データを JSON にまとめる

## 今回学ぶこと

- 辞書（名前をつけて値を管理する、リストの仲間）
- 47×47 のデータから「転入合計」「転出合計」「転入超過」を計算する
- `json` モジュールでファイルに保存する

## 辞書とは

リストは `prefectures[0]` のように**番号**で値を取り出しましたが、辞書は `"名前"` のような**キー**で値を取り出せる入れ物です。

```python
tokyo = {"name": "東京都", "net": 79285}
print(tokyo["name"])  # 東京都
print(tokyo["net"])   # 79285
```

`{キー: 値, キー: 値, ...}` の形で作ります。今回はこの後、「都道府県のリスト」「移動のリスト」「転入合計のリスト」などをまとめて1つの辞書に入れ、それをまるごと保存します。

## 47×47 のデータを Python のリストに読み込む

07 で学んだ二重ループを使って、47×47 のデータを「リストのリスト」（2次元のリスト）として読み込みます。`matrix[i][j]` で「i 番目の都道府県から j 番目の都道府県への移動者数」を表すことにします。

```python
def load_matrix(file_path):
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook["a002"]

    matrix = []
    for row_index in range(47):
        excel_row = 9 + row_index
        row_values = []
        for col_index in range(47):
            excel_col = 11 + col_index * 3
            value = sheet.cell(row=excel_row, column=excel_col).value
            if value == "-":
                value = 0
            row_values.append(value)
        matrix.append(row_values)

    return matrix
```

`04` で学んだ通り、これは1つの処理に名前をつけた**関数**です。ファイルパスを渡せば、いつでも同じ手順で読み込めます。

## flows（誰からどこへ何人か）のリストを作る

vis_peopleflow の JSON データは、`[転出元の番号, 転入先の番号, 人数]` という3つの値の組を、移動があった数だけ並べた `flows` というリストを持っていました。同じ形を自分たちのデータからも作ってみます。

```python
def build_flows(matrix):
    flows = []
    for from_index in range(47):
        for to_index in range(47):
            count = matrix[from_index][to_index]
            if count > 0:
                flows.append([from_index, to_index, count])
    return flows
```

`count > 0` で絞り込んでいるのは、同じ都道府県同士（対角成分、0 になっている）を除くためです。

## 転入合計・転出合計・転入超過を計算する

「転出元の行」を合計するとその県からの転出者数の合計に、「転入先の列」を合計するとその県への転入者数の合計になります。

```python
def build_in_out_net(matrix):
    in_totals = [0] * 47
    out_totals = [0] * 47

    for from_index in range(47):
        for to_index in range(47):
            count = matrix[from_index][to_index]
            out_totals[from_index] += count
            in_totals[to_index] += count

    net = []
    for i in range(47):
        net.append(in_totals[i] - out_totals[i])

    return in_totals, out_totals, net
```

`[0] * 47` は「0 が47個並んだリスト」を作る書き方です。あとから `out_totals[from_index] += count`（`+=` は「足してから入れ直す」の意味、`03` の `total = total + change` と同じことです）で少しずつ足し込んでいきます。

**この計算が正しいかどうかは、Excel の8行目にある公式の「総数」の値と比べて確かめられます。** 実際に 2024 年のデータで確認すると、北海道の転入合計は 53,281 人、転出合計は 59,566 人となり、これは総務省が公表している集計値とぴったり一致します。

## json で保存する

Python の辞書やリストを、そのままの形でファイルに保存できるのが `json` モジュールです。

```python
import json

data = {
    "prefs": PREFECTURES,
    "flows": flows,
    "in": in_totals,
    "out": out_totals,
    "net": net,
}

with open("data/processed/migration_2024.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
```

- `json.dump(データ, ファイル, ...)` で、辞書やリストをそのまま JSON という形式でファイルに書き出します。
- `ensure_ascii=False` を付けないと、日本語が `北海道` のような読めない文字コードで保存されてしまうので、必ず付けます。
- `indent=2` は見やすいように2文字分のインデントをつける指定です。なくても動きますが、人間が中身を確認しやすくなります。

これで作られる `migration_2024.json` は、`prefs`（都道府県名のリスト）・`flows`・`in`・`out`・`net` を持つ、vis_peopleflow の `migration_data.json` とほぼ同じ構造のデータになります。

## 実際に動かしてみる

```
uv run python steps/08_build_json.py
```

`data/processed/migration_2024.json` ができます。エディタで開いて中身を眺めてみましょう。ファイルの先頭のほうに `"prefs"` や `"flows"` が見つかるはずです。

## 演習

1. できあがった JSON を開いて、`"net"` の一番大きい値と一番小さい値がどの都道府県か、目で探してみましょう（09 でこれをグラフにします）。
2. `build_flows` の `if count > 0` を `if count > 1000` に変えると、`flows` の件数がどう変わるか試してみましょう。

次は [09. matplotlib で棒グラフ](09_visualize_bar.md) に進んでください。
