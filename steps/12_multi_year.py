import json
from pathlib import Path

import japanize_matplotlib  # noqa: F401  (import するだけで日本語フォント設定が有効になる)
import matplotlib.pyplot as plt
import openpyxl

PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県",
]


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


def calc_net(matrix):
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

    return net


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

output = {
    "prefs": PREFECTURES,
    "years": {str(year): net for year, net in net_by_year.items()},
}

with open("data/processed/migration_all.json", "w", encoding="utf-8") as file:
    json.dump(output, file, ensure_ascii=False, indent=2)

print("保存しました: data/processed/migration_all.json")

tokyo_index = PREFECTURES.index("東京都")
years_list = sorted(net_by_year.keys())
tokyo_net = [net_by_year[year][tokyo_index] for year in years_list]

plt.plot(years_list, tokyo_net, marker="o")
plt.xticks(years_list)
plt.ylabel("転入超過数（人）")
plt.title("東京都の転入超過数の推移")
plt.savefig("data/processed/trend.png")

print("保存しました: data/processed/trend.png")
