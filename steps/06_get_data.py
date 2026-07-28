import argparse
from pathlib import Path
from urllib.request import Request, urlopen


DOWNLOAD_URLS = {
    2020: "https://www.e-stat.go.jp/stat-search/file-download?fileKind=0&statInfId=000032047082",
    2021: "https://www.e-stat.go.jp/stat-search/file-download?fileKind=0&statInfId=000032163815",
    2022: "https://www.e-stat.go.jp/stat-search/file-download?fileKind=0&statInfId=000040008241",
    2024: "https://www.e-stat.go.jp/stat-search/file-download?fileKind=0&statInfId=000040243447",
}


def download(year, force=False):
    output_path = Path(f"data/raw/idou_{year}.xlsx")
    if output_path.exists() and not force:
        print(f"{output_path} はすでに存在するためスキップします")
        return

    request = Request(
        DOWNLOAD_URLS[year],
        headers={"User-Agent": "move-out-in data downloader"},
    )
    with urlopen(request) as response:
        content = response.read()

    if not content.startswith(b"PK"):
        raise RuntimeError(f"{year}年のダウンロード結果がExcelファイルではありません")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)
    print(f"保存しました: {output_path}")


parser = argparse.ArgumentParser(description="e-Stat の住民基本台帳人口移動報告を取得します")
parser.add_argument(
    "years",
    nargs="*",
    type=int,
    help="取得する年（省略すると登録済みの年をすべて取得）",
)
parser.add_argument(
    "--force",
    action="store_true",
    help="既存のファイルがあっても上書きする",
)
args = parser.parse_args()

years = args.years or list(DOWNLOAD_URLS)
unknown_years = sorted(set(years) - DOWNLOAD_URLS.keys())
if unknown_years:
    parser.error(
        "URLが登録されていない年です: "
        + ", ".join(str(year) for year in unknown_years)
    )

for year in years:
    download(year, force=args.force)
