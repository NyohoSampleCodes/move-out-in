# move-out-in

都道府県間の人口移動（転入・転出）データを取得し、JSON に整形して可視化するまでを、Python 初心者向けに一段ずつ学びながら進めるプロジェクトです。

参考にした可視化: [vis_peopleflow](https://klareswasser.github.io/vis_peopleflow/) ([リポジトリ](https://github.com/klareswasser/vis_peopleflow/))

## 進め方

`docs/00_overview.md` から順番に読んでください。各回のテキストは `docs/`、対応する実行コードは `steps/` に、番号を揃えて置いてあります。

| ドキュメント | 内容 |
| --- | --- |
| [docs/00_overview.md](docs/00_overview.md) | 全体の目標とロードマップ |
| [docs/01_setup.md](docs/01_setup.md) | 環境確認（uv） |
| [docs/02_variables.md](docs/02_variables.md) | 変数・print |
| [docs/03_lists_and_loops.md](docs/03_lists_and_loops.md) | リスト・for文 |
| [docs/04_functions.md](docs/04_functions.md) | 関数の定義 |
| [docs/05_file_io.md](docs/05_file_io.md) | ファイルの読み書き |
| [docs/06_get_data.md](docs/06_get_data.md) | e-Stat から元データを入手する |
| [docs/07_read_excel.md](docs/07_read_excel.md) | openpyxl で Excel を読む |
| [docs/08_build_json.md](docs/08_build_json.md) | 辞書と json でデータを整形する |
| [docs/09_visualize_bar.md](docs/09_visualize_bar.md) | matplotlib で棒グラフ |
| [docs/10_visualize_interactive.md](docs/10_visualize_interactive.md) | plotly でインタラクティブな図（サンキー） |
| [docs/11_visualize_circular.md](docs/11_visualize_circular.md) | 円環レイアウト＋ Dash による hover 連動 |
| [docs/12_multi_year.md](docs/12_multi_year.md) | 複数年データへの拡張 |
| [docs/13_next_steps.md](docs/13_next_steps.md) | まとめと発展課題 |

## 開発メモ（学習ステップ外）

- [docs/note_smooth_flow_animation.md](docs/note_smooth_flow_animation.md) — vis_peopleflow が流れるアニメーションを CSS だけで滑らかに実現している仕組みと、Dash で同じことをやるための道筋

## ディレクトリ構成

- `docs/` — 学習用テキスト（読む順に番号付き）
- `steps/` — 各回に対応する練習・サンプルコード
- `data/raw/` — e-Stat からダウンロードした元データ（Excel、Git 管理外。`steps/06_get_data.py` で再取得する）
- `data/processed/` — コードから生成する JSON・画像・HTML（git 管理しない、再生成可能なため）

## 実行方法

Python の実行・パッケージ管理には [uv](https://docs.astral.sh/uv/) を使います。ライブラリを追加するときも `pip install` ではなく `uv add <package>` を使ってください。

```
uv run python steps/02_variables.py
```

## コードを書くときの方針

- コメントは「なぜそうしているか」が非自明なときだけ書く（例: Excel のセル番地の理由、対角成分が `-` になる理由）。読めばわかることは書かない。
- 各 `steps/*.py` はそのステップ単体で読んで動くことを優先し、共通処理の抽出は行わない（重複よりも読みやすさを優先）。
