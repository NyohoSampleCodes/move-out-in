import json

import japanize_matplotlib  # noqa: F401  (import するだけで日本語フォント設定が有効になる)
import matplotlib.pyplot as plt

with open("data/processed/migration_2024.json", encoding="utf-8") as file:
    data = json.load(file)

prefs = data["prefs"]
net = data["net"]

colors = []
for value in net:
    if value >= 0:
        colors.append("tab:red")
    else:
        colors.append("tab:blue")

plt.figure(figsize=(14, 6))
plt.bar(prefs, net, color=colors)
plt.xticks(rotation=90)
plt.ylabel("転入超過数（人）")
plt.title("都道府県別 転入超過数 (2024年)")
plt.tight_layout()
plt.savefig("data/processed/net_2024.png")

print("保存しました: data/processed/net_2024.png")
