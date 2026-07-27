# 知見メモ: 滑らかな流れアニメーションを実現するには

`11_visualize_circular.md` の本編には含めていない、開発中に得た技術的な知見のメモ。将来このプロジェクトのアニメーションを作り直すときのために残しておく。

## 背景

`11` で、hover した都道府県の転出・転入を示す弧の上にドットを動かすアニメーションを、Dash の `dcc.Interval` で実装した。しかし実際に動かすと、更新間隔を伸ばしても「サーバーへの問い合わせ（loading）が頻繁に走る」「動きがスムーズでない」という問題が解消しなかった。最終的にこの方式でのアニメーションは諦め、`11` 本編では半透明の弧を重ねるだけの静的な表現に落ち着いている。

## vis_peopleflow はどう実装しているか

参考にした [vis_peopleflow](https://klareswasser.github.io/vis_peopleflow/) の `pref_migration_ring.html` を直接確認したところ、「流れる点線」は座標を再計算するアニメーションではなく、**CSS だけで実装されていた**。

```css
@keyframes flow-dash {
  from { stroke-dashoffset: 0; }
  to   { stroke-dashoffset: -24; }
}
.flow.anim {
  stroke-dasharray: 6 18;             /* 実線6px・隙間18pxの破線パターン */
  animation: flow-dash 1.6s linear infinite;
}
.flow.anim.fast { animation-duration: .9s; }  /* 移動量が多い流れは速く */
```

SVG の線に `stroke-dasharray`（破線パターン）を指定し、その `stroke-dashoffset`（パターンをどれだけずらすか）を CSS の `@keyframes` で連続的に変化させている。パターンの繰り返し幅（`6+18=24`）ぶんちょうどオフセットさせて無限ループさせることで、破線が線に沿って流れているように見える。

さらに `.flow { mix-blend-mode: screen; }` も指定されていて、暗い背景の上で線が重なるほど明るくなる効果を出している（このプロジェクトで「半透明を重ねて色を濃くする」とやったことの、ダークテーマ向けバージョンにあたる）。

## なぜこちらの方が滑らかなのか

CSS アニメーション（`@keyframes`）は、ブラウザのレンダリングエンジンが GPU を使って直接処理する。JavaScript のタイマーで座標を計算し直す必要も、ましてやサーバーと通信する必要もない。

対して `11` の Dash 版は、アニメーションのひとコマごとに

1. `dcc.Interval` がサーバーに問い合わせを送る
2. サーバー側の Python が 90 本以上の弧を含む `figure` 全体を再計算する
3. その `figure` を JSON にしてブラウザへ送り返す
4. ブラウザの plotly.js が受け取った `figure` で画面を再描画する

という重い処理を繰り返す必要があった。これは構造的に CSS アニメーションとは比べ物にならないコストがかかる。今回の「カクつき」は実装の詰めが甘かったからというより、**Dash でサーバー往復方式のアニメーションを作る限り避けられない制約** だったと考えられる。

## Dash / plotly でも同じことをやるには

plotly.js が生成する SVG の `<path>` 要素に対して、`stroke-dasharray` と `@keyframes` を直接適用できれば、同じ滑らかさを再現できる可能性がある。ただし Dash の標準的な使い方（Python 側で `figure` を組み立てて返す）の外に出る必要があり、次のような手順が要る。

1. Dash の [`clientside_callback`](https://dash.plotly.com/clientside-callbacks) を使って、ブラウザ側で実行される JavaScript を登録する
2. figure が更新されて plotly.js が SVG を描き直すたびに、対象の `<path>` 要素（`.js-plotly-plot .scatterlayer path` あたり）に CSS クラスを付け直す
3. そのクラスに対応する `@keyframes` を、`app.css` などの静的アセットとして用意しておく

これは Python だけで完結する範囲を超え、ブラウザの DOM 構造と CSS の知識が新たに必要になる。今回のプロジェクトの「Python 初心者向け」という前提からは外れるため本編には含めなかったが、Dash と CSS アニメーションを組み合わせる発展的な題材として、いつか挑戦する価値はある。

## 参考

- vis_peopleflow のソース: [`pref_migration_ring.html`](https://github.com/klareswasser/vis_peopleflow/blob/main/pref_migration_ring.html)
- MDN: [CSS のアニメーション](https://developer.mozilla.org/ja/docs/Web/CSS/CSS_animations/Using_CSS_animations)
- MDN: [`stroke-dasharray`](https://developer.mozilla.org/ja/docs/Web/SVG/Reference/Attribute/stroke-dasharray) / [`stroke-dashoffset`](https://developer.mozilla.org/ja/docs/Web/SVG/Reference/Attribute/stroke-dashoffset)
- Dash 公式: [Clientside Callbacks](https://dash.plotly.com/clientside-callbacks)
