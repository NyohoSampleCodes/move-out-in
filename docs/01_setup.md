# 01. 環境の確認

## uv とは

このプロジェクトでは、Python 本体やライブラリの管理に **uv** というツールを使います。uv は、

- どのバージョンの Python を使うか
- どんな外部ライブラリ（openpyxl や matplotlib など）が必要か

を `pyproject.toml` というファイルに記録しておき、`uv run` と打つだけで「必要なものが全部揃った状態」で Python を実行してくれる道具です。自分のパソコンの Python 環境を汚さずに済むので、迷ったら uv 経由でコマンドを実行する、と覚えておいてください。

## インストールされているか確認する

ターミナルで次のコマンドを実行してください。

```
uv --version
```

バージョン番号（例: `uv 0.11.29`）が表示されれば大丈夫です。何も表示されない・エラーになる場合は、[uv 公式サイト](https://docs.astral.sh/uv/getting-started/installation/)の手順に従ってインストールしてください。

## このプロジェクトの Python を動かしてみる

プロジェクトのフォルダ（`move-out-in`）の中で、次のコマンドを実行してみましょう。

```
uv run python --version
```

`Python 3.12.x` のように表示されれば準備完了です。裏側では、`pyproject.toml` に書かれたバージョンの Python が自動的に用意されています。

## コードの実行方法

これから `steps/` フォルダに、回ごとのコードを置いていきます。実行するときは、必ず `uv run python` の後ろにファイルのパスを続けてください。

```
uv run python steps/02_variables.py
```

`uv run` を付けずに `python steps/02_variables.py` のように直接実行すると、このプロジェクト用に用意したライブラリ（openpyxl や matplotlib など）が見つからずエラーになることがあります。迷ったら `uv run` を付ける、と覚えておけば大丈夫です。

## ディレクトリの中身

| フォルダ / ファイル | 役割 |
| --- | --- |
| `docs/` | このテキスト |
| `steps/` | 回ごとのサンプルコード |
| `data/raw/` | ダウンロードした元データ（Excel、Git 管理外） |
| `data/processed/` | コードを実行して生成される JSON やグラフ |
| `pyproject.toml` | 使う Python のバージョンやライブラリの一覧 |

次は [02. 変数と print](02_variables.md) に進んでください。
