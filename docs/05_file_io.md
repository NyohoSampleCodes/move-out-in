# 05. ファイルの読み書き

## 今回学ぶこと

- `open()` でファイルを開く
- ファイルへの書き込み・読み込み
- `with` 文（ファイルの閉じ忘れを防ぐ書き方）

## なぜファイルに保存するのか

ここまでのステップで作った値は、プログラムを終了すると消えてしまいます。あとで何度も使うデータ（今回は都道府県の人口移動データ）は、ファイルに保存しておく必要があります。この回では、まず仕組みを理解するために簡単なテキストファイルで練習し、07 以降で本物のデータを読み書きします。

## ファイルに書き込む

```python
file = open("data/processed/hello.txt", "w", encoding="utf-8")
file.write("こんにちは\n")
file.write("北海道\n")
file.close()
```

- `open(ファイル名, "w", encoding="utf-8")` で、書き込み（write）モードでファイルを開きます。`"w"` で開くと、そのファイルがすでにあっても中身は空になるので注意してください。
- `encoding="utf-8"` は、日本語を正しく保存するためのおまじないだと思ってください。
- `file.write(...)` で1行ずつ書き込みます。`\n` は改行を表します。
- 書き終わったら `file.close()` でファイルを閉じます。**閉じ忘れると、書き込んだ内容がファイルにきちんと保存されないことがあります。**

## with 文を使うと閉じ忘れない

`close()` を書き忘れる事故を防ぐため、実際には `with` 文を使うのが一般的です。

```python
with open("data/processed/hello.txt", "w", encoding="utf-8") as file:
    file.write("こんにちは\n")
    file.write("北海道\n")
# ここまで来ると、自動的にファイルが閉じられている
```

`with ... as file:` のブロック（インデントされた部分）を抜けると、自動的に `file.close()` が呼ばれます。これ以降、このプロジェクトのコードはすべて `with` 文でファイルを扱います。

## ファイルを読み込む

```python
with open("data/processed/hello.txt", "r", encoding="utf-8") as file:
    content = file.read()

print(content)
```

`"r"`（read、読み込み）モードで開き、`file.read()` でファイルの中身をすべて文字列として受け取ります。

1行ずつ読みたいときは、`for` 文でファイルをそのまま回すこともできます。

```python
with open("data/processed/hello.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.strip())
```

`line` の末尾には改行文字 `\n` が含まれているので、`.strip()` で取り除いています。

## 実際に動かしてみる

```
uv run python steps/05_file_io.py
```

実行すると `data/processed/hello.txt` が作られます。エディタで開いて中身を確認してみましょう。

## 演習

1. `03` で作った `ALL_PREFECTURES` のリストを、1行に1つずつファイルに書き出してみましょう。
2. 書き出したファイルを読み込み直して、`for` 文で画面に表示してみましょう。

次は [06. データの入手](06_get_data.md) に進んでください。
