import json

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


def build_flows(matrix):
    flows = []
    for from_index in range(47):
        for to_index in range(47):
            count = matrix[from_index][to_index]
            if count > 0:
                flows.append([from_index, to_index, count])
    return flows


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


matrix = load_matrix("data/raw/idou_2024.xlsx")
flows = build_flows(matrix)
in_totals, out_totals, net = build_in_out_net(matrix)

# 公式の集計値と一致するか確認（北海道: 転入53281人、転出59566人のはず）
print("北海道 転入:", in_totals[0], "転出:", out_totals[0])

data = {
    "prefs": PREFECTURES,
    "flows": flows,
    "in": in_totals,
    "out": out_totals,
    "net": net,
}

with open("data/processed/migration_2024.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("flowsの件数:", len(flows))
print("保存しました: data/processed/migration_2024.json")
