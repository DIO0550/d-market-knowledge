# 図の作り方（インラインSVG）

技術参考書の図は**インラインSVG**で描く。ベクタなので拡大しても劣化せず、
PDF内でテキストとして保持されるため検索にも引っかかる。

## 鉄則：スタイルはSVGの中に書く

**WeasyPrintは外部CSS（`book.css`）をインラインSVGに適用しない。**
`class="dia-box"` と書いても効かず、矩形は黒く塗り潰される。`currentColor` も継承されない。

指定方法は次の3つ。どれを使ってもよいが、**必ずSVGの内側**で完結させる。

```html
<!-- 1. SVG内の<style>（要素数が多い図に向く） -->
<svg viewBox="0 0 420 150"><style>.box { fill: #e8f0f9; stroke: #1b4f8a; }</style>…</svg>

<!-- 2. 属性で直接指定（単純な図に向く） -->
<rect fill="#e8f0f9" stroke="#1b4f8a" stroke-width="1.2"/>

<!-- 3. <g>でまとめて継承（同じ体裁の要素が並ぶとき） -->
<g fill="#e8f0f9" stroke="#1b4f8a" stroke-width="1.2">…</g>
```

## 共通スタイル

各図の先頭にこれを貼る。`--accent` を変えた場合は色をそこに合わせる。

```html
<style>
  .box   { fill: #e8f0f9; stroke: #1b4f8a; stroke-width: 1.2; }
  .box-w { fill: #ffffff; stroke: #1b4f8a; stroke-width: 1.2; }
  .box-a { fill: #fff7e6; stroke: #e0a94a; stroke-width: 1.2; }
  .line  { stroke: #1b4f8a; stroke-width: 1.4; fill: none; }
  .dash  { stroke: #1b4f8a; stroke-width: 1.2; fill: none; stroke-dasharray: 5 3; }
  .thin  { stroke: #c8ced6; stroke-width: 0.8; fill: none; }
  .t     { font-family: "Noto Sans CJK JP"; font-size: 11px; fill: #1a1a1a; }
  .t-s   { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #5a5f66; }
  .t-b   { font-family: "Noto Sans CJK JP"; font-size: 11px; fill: #1b4f8a; font-weight: 700; }
</style>
<defs>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#1b4f8a"/>
  </marker>
</defs>
```

矢印は `marker-end="url(#ah)"` で付ける。`id` はSVGごとに閉じているため、
複数の図で同じ `ah` を使い回しても両方きちんと描画される（検証済み）。
ただし他のレンダラに持ち込む可能性を考えるなら `ah1` `ah2` と連番にしておくと無難。

## 寸法の決め方

- `viewBox` だけを書き、`width` / `height` 属性は書かない。版面幅にCSSで合わせる。
- `viewBox` の幅は **420** で固定すると考えやすい（この値が版面いっぱいになる）。
- 高さは内容次第だが、**420×280を超えると1ページに収まりにくい**。超えるなら図を分割する。

**文字サイズは版面幅で圧縮されることを忘れない。** `viewBox` 幅420が版面幅に収まるので、
指定したpx値はそのまま出ない。実寸は次のとおり。

| SVGの指定 | a4 | b5 | a5 |
|---|---|---|---|
| `font-size: 11px` | 10.2pt | 8.8pt | 7.2pt |
| `font-size: 9px`  | 8.4pt  | 7.2pt | 5.9pt |
| `font-size: 7.5px`| 7.0pt  | 6.0pt | 4.9pt |

**主ラベルは11px、補助ラベルは9px**を下限とする。7.5pxはb5で6pt、a5で5ptまで潰れて
印刷では読めない。a5で図を多用するなら `viewBox` 幅を340まで狭めて相対的に文字を大きくする。

## パターン1：構成図（往復のやり取り）

```html
<figure class="fig">
<svg viewBox="0 0 420 110" xmlns="http://www.w3.org/2000/svg">
  <style>
    .box { fill: #e8f0f9; stroke: #1b4f8a; stroke-width: 1.2; }
    .t { font-family: "Noto Sans CJK JP"; font-size: 11px; fill: #1a1a1a; }
    .t-s { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #5a5f66; }
  </style>
  <defs><marker id="ah1" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#1b4f8a"/></marker></defs>

  <rect class="box" x="10" y="30" width="110" height="50" rx="4"/>
  <text class="t" x="65" y="60" text-anchor="middle">クライアント</text>

  <rect class="box" x="300" y="30" width="110" height="50" rx="4"/>
  <text class="t" x="355" y="60" text-anchor="middle">サーバ</text>

  <line x1="125" y1="46" x2="295" y2="46"
        stroke="#1b4f8a" stroke-width="1.4" marker-end="url(#ah1)"/>
  <text class="t-s" x="210" y="40" text-anchor="middle">リクエスト</text>

  <line x1="295" y1="66" x2="125" y2="66" stroke="#1b4f8a" stroke-width="1.2"
        stroke-dasharray="5 3" marker-end="url(#ah1)"/>
  <text class="t-s" x="210" y="80" text-anchor="middle">レスポンス</text>
</svg>
<figcaption>HTTPの往復構造</figcaption>
</figure>
```

## パターン2：シーケンス図（時間の流れ）

縦のライフラインに沿って番号付きのやり取りを並べる。プロトコルの説明に使う。

```html
<figure class="fig">
<svg viewBox="0 0 420 200" xmlns="http://www.w3.org/2000/svg">
  <style>
    .head { fill: #1b4f8a; }
    .ht { font-family: "Noto Sans CJK JP"; font-size: 10px; fill: #ffffff; }
    .life { stroke: #c8ced6; stroke-width: 0.8; stroke-dasharray: 3 3; }
    .t-s { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #1a1a1a; }
    .num { font-family: "Noto Sans CJK JP"; font-size: 8.5px; fill: #ffffff; }
  </style>
  <defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#1b4f8a"/></marker></defs>

  <rect class="head" x="20" y="8" width="110" height="24" rx="3"/>
  <text class="ht" x="75" y="24" text-anchor="middle">ブラウザ</text>
  <line class="life" x1="75" y1="32" x2="75" y2="192"/>

  <rect class="head" x="290" y="8" width="110" height="24" rx="3"/>
  <text class="ht" x="345" y="24" text-anchor="middle">サーバ</text>
  <line class="life" x1="345" y1="32" x2="345" y2="192"/>

  <!-- 1本のやり取り = 矢印 + 番号バッジ + ラベル。y座標を40ずつ下げて繰り返す -->
  <line x1="75" y1="60" x2="345" y2="60"
        stroke="#1b4f8a" stroke-width="1.4" marker-end="url(#ah2)"/>
  <circle cx="88" cy="52" r="7" fill="#1b4f8a"/>
  <text class="num" x="88" y="55" text-anchor="middle">1</text>
  <text class="t-s" x="210" y="55" text-anchor="middle">GET /index.html</text>

  <line x1="345" y1="100" x2="75" y2="100" stroke="#1b4f8a" stroke-width="1.2"
        stroke-dasharray="5 3" marker-end="url(#ah2)"/>
  <circle cx="332" cy="92" r="7" fill="#1b4f8a"/>
  <text class="num" x="332" y="95" text-anchor="middle">2</text>
  <text class="t-s" x="210" y="95" text-anchor="middle">200 OK + HTML</text>
</svg>
<figcaption>ページ取得のシーケンス</figcaption>
</figure>
```

## パターン3：レイヤ図（階層構造）

プロトコルスタックやアーキテクチャの層を示す。

```html
<figure class="fig">
<svg viewBox="0 0 420 160" xmlns="http://www.w3.org/2000/svg">
  <style>
    .l { stroke: #1b4f8a; stroke-width: 1.2; }
    .t { font-family: "Noto Sans CJK JP"; font-size: 11px; fill: #1a1a1a; }
    .t-s { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #5a5f66; }
  </style>
  <rect class="l" x="60" y="10"  width="300" height="34" fill="#d6e4f2"/>
  <text class="t" x="210" y="31" text-anchor="middle">アプリケーション層（HTTP）</text>
  <rect class="l" x="60" y="44"  width="300" height="34" fill="#e8f0f9"/>
  <text class="t" x="210" y="65" text-anchor="middle">トランスポート層（TCP）</text>
  <rect class="l" x="60" y="78"  width="300" height="34" fill="#f2f6fb"/>
  <text class="t" x="210" y="99" text-anchor="middle">インターネット層（IP）</text>
  <rect class="l" x="60" y="112" width="300" height="34" fill="#ffffff"/>
  <text class="t" x="210" y="133" text-anchor="middle">リンク層（Ethernet）</text>
  <text class="t-s" x="50" y="31" text-anchor="end">上位</text>
  <text class="t-s" x="50" y="133" text-anchor="end">下位</text>
</svg>
<figcaption>TCP/IPの4階層モデル</figcaption>
</figure>
```

## パターン4：フロー図（分岐のある処理）

```html
<figure class="fig">
<svg viewBox="0 0 420 190" xmlns="http://www.w3.org/2000/svg">
  <style>
    .box { fill: #e8f0f9; stroke: #1b4f8a; stroke-width: 1.2; }
    .dec { fill: #fff7e6; stroke: #e0a94a; stroke-width: 1.2; }
    .t { font-family: "Noto Sans CJK JP"; font-size: 10px; fill: #1a1a1a; }
    .t-s { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #5a5f66; }
  </style>
  <defs><marker id="ah4" viewBox="0 0 10 10" refX="9" refY="5"
        markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#1b4f8a"/></marker></defs>

  <rect class="box" x="150" y="8" width="120" height="30" rx="4"/>
  <text class="t" x="210" y="27" text-anchor="middle">リクエスト受信</text>
  <line x1="210" y1="38" x2="210" y2="58"
        stroke="#1b4f8a" stroke-width="1.4" marker-end="url(#ah4)"/>

  <path class="dec" d="M210,60 L290,95 L210,130 L130,95 z"/>
  <text class="t" x="210" y="98" text-anchor="middle">キャッシュあり？</text>

  <line x1="290" y1="95" x2="345" y2="95"
        stroke="#1b4f8a" stroke-width="1.4" marker-end="url(#ah4)"/>
  <text class="t-s" x="317" y="88" text-anchor="middle">Yes</text>
  <rect class="box" x="345" y="78" width="70" height="34" rx="4"/>
  <text class="t" x="380" y="99" text-anchor="middle">再利用</text>

  <line x1="210" y1="130" x2="210" y2="152"
        stroke="#1b4f8a" stroke-width="1.4" marker-end="url(#ah4)"/>
  <text class="t-s" x="222" y="145">No</text>
  <rect class="box" x="150" y="152" width="120" height="30" rx="4"/>
  <text class="t" x="210" y="171" text-anchor="middle">オリジンへ問い合わせ</text>
</svg>
<figcaption>キャッシュ判定の流れ</figcaption>
</figure>
```

## アイコン集（セキュリティ図・構成図用）

人物や機器のアイコンは `<defs>` に置き、`<use href="#id" x= y= class=>` で呼び出す。
`<use>` はWeasyPrintで動作する（`xlink:href` でも可）。塗り色は `<use>` 側の
`class` / `fill` で切り替えられるので、同じ形を利用者は青・攻撃者は赤で使い分けられる。

各アイコンは**40×50の枠**に収めてある。`x` `y` は左上の座標。

```html
<defs>
  <!-- 利用者・一般人物 -->
  <g id="person">
    <circle cx="20" cy="11" r="9"/>
    <path d="M2,48 C2,33 9,26 20,26 C31,26 38,33 38,48 Z"/>
  </g>

  <!-- 攻撃者（フード＋目線マスク） -->
  <g id="attacker">
    <path d="M20,0 C10,0 6,6 6,13 L34,13 C34,6 30,0 20,0 Z" fill="#7a3512"/>
    <circle cx="20" cy="13" r="9"/>
    <rect x="10" y="11" width="20" height="4.5" rx="1" fill="#ffffff"/>
    <path d="M2,50 C2,35 9,28 20,28 C31,28 38,35 38,50 Z"/>
  </g>

  <!-- サーバ -->
  <g id="server">
    <rect x="4" y="4" width="32" height="44" rx="3"/>
    <rect x="9" y="11" width="22" height="4" rx="1" fill="#ffffff"/>
    <rect x="9" y="20" width="22" height="4" rx="1" fill="#ffffff"/>
    <rect x="9" y="29" width="22" height="4" rx="1" fill="#ffffff"/>
  </g>

  <!-- PC・ブラウザ -->
  <g id="pc">
    <rect x="2" y="6" width="36" height="26" rx="2"/>
    <rect x="6" y="10" width="28" height="18" fill="#ffffff"/>
    <path d="M12,36 L28,36 L32,44 L8,44 Z"/>
  </g>

  <!-- データベース -->
  <g id="db">
    <ellipse cx="20" cy="9" rx="17" ry="6"/>
    <path d="M3,9 L3,39 C3,42.3 10.6,45 20,45 C29.4,45 37,42.3 37,39 L37,9
             C37,12.3 29.4,15 20,15 C10.6,15 3,12.3 3,9 Z"/>
    <ellipse cx="20" cy="25" rx="17" ry="6" fill="none" stroke="#ffffff" stroke-width="1.4"/>
  </g>

  <!-- 錠前（暗号化・保護） -->
  <g id="lock">
    <rect x="5" y="20" width="30" height="26" rx="3"/>
    <path d="M11,20 L11,13 C11,8 15,4 20,4 C25,4 29,8 29,13 L29,20"
          fill="none" stroke="#1b4f8a" stroke-width="4"/>
    <circle cx="20" cy="31" r="3.5" fill="#ffffff"/>
    <rect x="18.5" y="31" width="3" height="8" fill="#ffffff"/>
  </g>

  <!-- メール -->
  <g id="mail">
    <rect x="2" y="10" width="36" height="26" rx="2"/>
    <path d="M2,12 L20,26 L38,12" fill="none" stroke="#ffffff" stroke-width="1.8"/>
  </g>

  <!-- クラウド（56×42と横長。他より広い枠を取る） -->
  <g id="cloud">
    <path d="M11,38 C4,38 0,33 0,27 C0,21 5,17 10,17 C12,9 19,4 27,4
             C36,4 43,11 44,20 C51,21 55,26 55,31 C55,35 52,38 47,38 Z"/>
  </g>
</defs>
```

呼び出しはこう書く。

```html
<use href="#person" x="10" y="95" fill="#1b4f8a"/>
<use href="#attacker" x="190" y="80" fill="#b3541e"/>
```

`#lock` の掛け金だけは `stroke` を直書きしているので、主色を変えたときは
`stroke="#1b4f8a"` の値も合わせて書き換える。

## パターン5：攻撃フロー図（中間者攻撃）

セキュリティの説明では、**攻撃者を赤系（#b3541e）、正規の登場人物を主色**で塗り分けると
一目で立場が伝わる。攻撃者の活動範囲は破線の枠で囲む。

```html
<figure class="fig">
<svg viewBox="0 0 420 175" xmlns="http://www.w3.org/2000/svg">
  <style>
    .t   { font-family: "Noto Sans CJK JP"; font-size: 11px; fill: #1a1a1a; }
    .t-s { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #5a5f66; }
    .t-w { font-family: "Noto Sans CJK JP"; font-size: 9px; fill: #b3541e; font-weight: 700; }
    .num { font-family: "Noto Sans CJK JP"; font-size: 8.5px; fill: #ffffff; }
  </style>
  <defs>
    <g id="p1"><circle cx="20" cy="11" r="9"/>
      <path d="M2,48 C2,33 9,26 20,26 C31,26 38,33 38,48 Z"/></g>
    <g id="a1">
      <path d="M20,0 C10,0 6,6 6,13 L34,13 C34,6 30,0 20,0 Z" fill="#7a3512"/>
      <circle cx="20" cy="13" r="9"/>
      <rect x="10" y="11" width="20" height="4.5" rx="1" fill="#ffffff"/>
      <path d="M2,50 C2,35 9,28 20,28 C31,28 38,35 38,50 Z"/></g>
    <g id="s1"><rect x="4" y="4" width="32" height="44" rx="3"/>
      <rect x="9" y="11" width="22" height="4" rx="1" fill="#ffffff"/>
      <rect x="9" y="20" width="22" height="4" rx="1" fill="#ffffff"/>
      <rect x="9" y="29" width="22" height="4" rx="1" fill="#ffffff"/></g>
    <marker id="ah5" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7"
      orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b3541e"/></marker>
  </defs>

  <!-- 「直接つながっていると信じている」を示す破線ブラケット -->
  <text class="t-w" x="210" y="14" text-anchor="middle">利用者もサーバも「相手と直接つながっている」と信じている</text>
  <path d="M30,58 L30,22 L388,22 L388,58" fill="none"
        stroke="#c8ced6" stroke-width="0.8" stroke-dasharray="3 3"/>

  <use href="#p1" x="10" y="79" fill="#1b4f8a"/>
  <text class="t" x="30" y="144" text-anchor="middle">利用者</text>

  <rect x="160" y="54" width="100" height="76" rx="4" fill="#fdf1e7"
        stroke="#b3541e" stroke-width="1.2" stroke-dasharray="4 3"/>
  <use href="#a1" x="190" y="64" fill="#b3541e"/>
  <text class="t-w" x="210" y="126" text-anchor="middle">攻撃者（中間者）</text>

  <use href="#s1" x="370" y="79" fill="#1b4f8a"/>
  <text class="t" x="388" y="144" text-anchor="middle">Webサーバ</text>

  <line x1="55" y1="89" x2="155" y2="89" stroke="#b3541e" stroke-width="1.5" marker-end="url(#ah5)"/>
  <circle cx="68" cy="80" r="7" fill="#b3541e"/>
  <text class="num" x="68" y="83" text-anchor="middle">1</text>
  <text class="t-s" x="110" y="77" text-anchor="middle">通信を横取り</text>

  <line x1="265" y1="89" x2="365" y2="89" stroke="#b3541e" stroke-width="1.5" marker-end="url(#ah5)"/>
  <circle cx="278" cy="80" r="7" fill="#b3541e"/>
  <text class="num" x="278" y="83" text-anchor="middle">2</text>
  <text class="t-s" x="315" y="77" text-anchor="middle">正規を装って中継</text>

  <line x1="365" y1="109" x2="265" y2="109" stroke="#b3541e" stroke-width="1.2"
        stroke-dasharray="5 3" marker-end="url(#ah5)"/>
  <line x1="155" y1="109" x2="55" y2="109" stroke="#b3541e" stroke-width="1.2"
        stroke-dasharray="5 3" marker-end="url(#ah5)"/>
  <text class="t-s" x="210" y="147" text-anchor="middle">応答を盗み見・改ざんして返す</text>
</svg>
<figcaption>中間者攻撃（MITM）の成立条件</figcaption>
</figure>
```

攻撃図を出したら、**対になる対策図を続けて置く**と理解が定着する。対策図では
配色を主色に戻し、`#lock` アイコンや検証ステップを足して「どこで攻撃が止まるか」を示す。

## 確認事項

図を入れたら必ずPDFを画像化して目視する。特に次を見る。

- 日本語が豆腐（□）になっていないか — `font-family` はシステムにある名前と厳密に一致させる。
  SVG内`<style>`・属性指定・引用符の有無はいずれでも動く（検証済み）ので、書きやすい形でよい
- ラベルが枠からはみ出していないか — 和文は1文字あたり約`font-size`ぶんの幅を取る。
  11pxなら「クライアント」6文字で約66px。枠幅はその1.3倍を目安に取る
- 図が版面をはみ出していないか — `viewBox` の高さが280を超えていたら分割する
- **線と文字が重なっていないか** — 補助線の端点はラベルの上端から10単位以上離す。
  和文ラベルの高さは `font-size` とほぼ同じ、幅は `font-size × 文字数` で見積もる
