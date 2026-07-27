import json
import math

import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

with open("data/processed/migration_2024.json", encoding="utf-8") as file:
    data = json.load(file)

PREFS = data["prefs"]
FLOWS = data["flows"]
NET = data["net"]
N = len(PREFS)

NODE_RADIUS = 1.0
MAX_NET = max(abs(v) for v in NET)
BAR_SCALE = 0.4 / MAX_NET
MIN_FLOW_WIDTH = 0.8
MAX_FLOW_WIDTH = 4.0
# 半透明にしておくと、同じ場所を通る弧が多いところほど自然に重なって濃くなる
FLOW_OPACITY = 0.35
# 転出・転入の弧を左右にずらす幅。0 だと2本がぴったり重なってしまう
ARC_OFFSET = 0.15

# 都道府県ごとに関係する flows を仕分けておく（hover のたびに全件を探し直さないため）
OUT_FLOWS_BY_PREF = [[] for _ in range(N)]
IN_FLOWS_BY_PREF = [[] for _ in range(N)]
for from_index, to_index, count in FLOWS:
    OUT_FLOWS_BY_PREF[from_index].append((from_index, to_index, count))
    IN_FLOWS_BY_PREF[to_index].append((from_index, to_index, count))


def polar_to_xy(index, radius):
    # -pi/2 して、0番目（北海道）が真上から始まるようにしている
    angle = 2 * math.pi * index / N - math.pi / 2
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y


def bezier_points(p0, p1, control, n=30):
    xs = []
    ys = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * control[0] + t ** 2 * p1[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * control[1] + t ** 2 * p1[1]
        xs.append(x)
        ys.append(y)
    return xs, ys


def perpendicular_offset(base, target, amount):
    # base→target 方向に対して垂直なベクトルを返す。
    # 転出・転入で常に「hover 中の都道府県からの向き」を基準にしないと、
    # 符号を反転させても同じ側にずれてしまう。
    dx = target[0] - base[0]
    dy = target[1] - base[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return (0, 0)
    return (-dy / length * amount, dx / length * amount)


def build_node_trace():
    xs = []
    ys = []
    for i in range(N):
        x, y = polar_to_xy(i, NODE_RADIUS)
        xs.append(x)
        ys.append(y)
    return go.Scatter(
        x=xs, y=ys, mode="markers+text",
        text=PREFS, textposition="top center", textfont=dict(size=8),
        marker=dict(size=8, color="dimgray"),
        hovertemplate="%{text}<extra></extra>", showlegend=False,
    )


def build_bar_traces():
    increase_x, increase_y = [], []
    decrease_x, decrease_y = [], []
    for i in range(N):
        x0, y0 = polar_to_xy(i, NODE_RADIUS)
        x1, y1 = polar_to_xy(i, NODE_RADIUS + abs(NET[i]) * BAR_SCALE)
        if NET[i] >= 0:
            increase_x += [x0, x1, None]
            increase_y += [y0, y1, None]
        else:
            decrease_x += [x0, x1, None]
            decrease_y += [y0, y1, None]

    # 外周バーの色は、その都道府県が転入超過か転出超過か（＝正負）を表す
    increase_trace = go.Scatter(
        x=increase_x, y=increase_y, mode="lines",
        line=dict(color="crimson", width=6), hoverinfo="skip", showlegend=False,
    )
    decrease_trace = go.Scatter(
        x=decrease_x, y=decrease_y, mode="lines",
        line=dict(color="royalblue", width=6), hoverinfo="skip", showlegend=False,
    )
    return increase_trace, decrease_trace


def flow_width(count, max_count):
    return MIN_FLOW_WIDTH + (MAX_FLOW_WIDTH - MIN_FLOW_WIDTH) * (count / max_count)


def build_flow_traces(pref_index):
    # 半透明にした弧を描く。太さ＝移動者数、色＝転出/転入。
    # hover 中の都道府県のまわりでは、多くの弧が同じ場所を通って重なるので、
    # 自然と色が濃くなる。相手県に近づくほど弧は散らばるので薄いままになる。
    self_pos = polar_to_xy(pref_index, NODE_RADIUS)
    traces = []

    out_flows = OUT_FLOWS_BY_PREF[pref_index]
    if out_flows:
        max_out = max(count for _, _, count in out_flows)
        for i, (from_index, to_index, count) in enumerate(out_flows):
            other_pos = polar_to_xy(to_index, NODE_RADIUS)
            offset = perpendicular_offset(self_pos, other_pos, ARC_OFFSET)
            xs, ys = bezier_points(self_pos, other_pos, control=offset)
            traces.append(go.Scatter(
                x=xs, y=ys, mode="lines",
                line=dict(color="royalblue", width=flow_width(count, max_out)),
                opacity=FLOW_OPACITY, hoverinfo="skip",
                legendgroup="out", name="転出", showlegend=(i == 0),
            ))

    in_flows = IN_FLOWS_BY_PREF[pref_index]
    if in_flows:
        max_in = max(count for _, _, count in in_flows)
        for i, (from_index, to_index, count) in enumerate(in_flows):
            other_pos = polar_to_xy(from_index, NODE_RADIUS)
            # 転出とは逆向きにずらすことで、2本の弧が重ならないようにする
            offset = perpendicular_offset(self_pos, other_pos, -ARC_OFFSET)
            xs, ys = bezier_points(other_pos, self_pos, control=offset)
            traces.append(go.Scatter(
                x=xs, y=ys, mode="lines",
                line=dict(color="crimson", width=flow_width(count, max_in)),
                opacity=FLOW_OPACITY, hoverinfo="skip",
                legendgroup="in", name="転入", showlegend=(i == 0),
            ))

    return traces


def build_figure(pref_index=None):
    title = "都道府県間の人口移動（点にマウスを乗せると転入・転出を表示）"
    traces = [build_node_trace(), *build_bar_traces()]

    if pref_index is not None:
        title = f"{PREFS[pref_index]} の 転入(赤) / 転出(青)"
        traces += build_flow_traces(pref_index)

    fig = go.Figure(data=traces)
    fig.update_layout(
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        showlegend=True,
        legend=dict(x=0.02, y=0.98),
        title=title,
        width=800,
        height=800,
        plot_bgcolor="white",
    )
    return fig


app = Dash(__name__)

app.layout = html.Div([
    html.H3("都道府県間の人口移動（円環配置）"),
    dcc.Graph(id="chord-graph", figure=build_figure()),
])


@app.callback(
    Output("chord-graph", "figure"),
    Input("chord-graph", "hoverData"),
)
def on_hover(hover_data):
    if hover_data is None:
        return build_figure(None)

    point = hover_data["points"][0]
    if point.get("curveNumber") != 0:
        # 都道府県のノード（0番目の trace）以外は無視する
        return build_figure(None)

    pref_index = point["pointIndex"]
    return build_figure(pref_index)


if __name__ == "__main__":
    app.run(debug=False)
