prefectures = ["北海道", "青森県", "岩手県", "宮城県"]
print(prefectures)
print(prefectures[0])
print(prefectures[1])

for prefecture in prefectures:
    print(prefecture)

print(len(prefectures))

net_changes = [-8637, -3080, -3080, 500]

total = 0
for change in net_changes:
    total = total + change

print(total)

# 47都道府県すべて。都道府県コード順（北海道〜沖縄県）。
# このあとのステップでも同じ並び順のリストを使う。
ALL_PREFECTURES = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県", "岐阜県",
    "静岡県", "愛知県", "三重県", "滋賀県", "京都府", "大阪府", "兵庫県",
    "奈良県", "和歌山県", "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県", "福岡県", "佐賀県", "長崎県",
    "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県",
]
print(len(ALL_PREFECTURES), "都道府県")
for prefecture in ALL_PREFECTURES:
    print(prefecture, "の人口は減っています")
