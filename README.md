# move-out-in

都道府県のあいだで、どのくらいの人が引っ越しているのか（転入・転出）を、自分の手でデータを取ってきて可視化してみるプロジェクトです。

こちらの可視化に憧れて、それを自分でも作れるようになることを目標にしています。

- 完成イメージ: [vis_peopleflow（デモ）](https://klareswasser.github.io/vis_peopleflow/)
- 元にしたソースコード: [vis_peopleflow（GitHub）](https://github.com/klareswasser/vis_peopleflow/)

いきなり同じものを作るのは難しいので、このプロジェクトでは

1. Python の基本（変数・リスト・ファイル入出力・関数）
2. 総務省統計局が公開している本物のデータを取ってくる
3. データを Python で読み込んで、扱いやすい形（JSON）に整形する
4. グラフやインタラクティブな図として可視化する

という順番で、一段ずつ進みます。**Python を書いたことがない人でも読み進められるように、テキストを用意してあります。**

## はじめに読むもの

このプロジェクトの進め方・全体構成は [AGENTS.md](AGENTS.md) にまとまっています。学習は [docs/00_overview.md](docs/00_overview.md) から始めてください。

## 必要なもの

- [uv](https://docs.astral.sh/uv/)（Python 本体とライブラリの管理に使います。インストール方法は [docs/01_setup.md](docs/01_setup.md) 参照）
