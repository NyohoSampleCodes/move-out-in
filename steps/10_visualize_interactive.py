import json

import plotly.graph_objects as go

with open("data/processed/migration_2024.json", encoding="utf-8") as file:
    data = json.load(file)

prefs = data["prefs"]
flows = data["flows"]

sorted_flows = sorted(flows, key=lambda flow: flow[2], reverse=True)
top_flows = sorted_flows[:30]

sources = [flow[0] for flow in top_flows]
targets = [flow[1] for flow in top_flows]
values = [flow[2] for flow in top_flows]

fig = go.Figure(data=[go.Sankey(
    node=dict(label=prefs, pad=10, thickness=15),
    link=dict(source=sources, target=targets, value=values),
)])
fig.update_layout(title_text="都道府県間の人口移動 上位30 (2024年)", font_size=10)
fig.write_html("data/processed/flows_2024.html")

print("保存しました: data/processed/flows_2024.html")
