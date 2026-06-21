# コンポーネントリファレンス

新テンプレート（学術ノート風ライトテーマ）のコンポーネント集。HTMLパターンとCSSクラスの使い方を詳細に示す。

## 目次

1. [レイアウト要素](#1-レイアウト要素)
2. [タイトルブロック](#2-タイトルブロック)
3. [左サイドバーTOC](#3-左サイドバーtoc)
4. [概要セクション（Overview）](#4-概要セクションoverview)
5. [コンテンツセクション](#5-コンテンツセクション)
6. [Callout（情報ボックス）](#6-callout情報ボックス)
7. [コード・数式](#7-コード数式)
8. [テーブル・タグ](#8-テーブルタグ)
9. [リスト](#9-リスト)
10. [Compare（2カラム比較）](#10-compare2カラム比較)
11. [Summary（まとめカードグリッド）](#11-summaryまとめカードグリッド)
12. [プログレスバー](#12-プログレスバー)
13. [アイコン（SVGと絵文字の使い分け）](#13-アイコンsvgと絵文字の使い分け)

---

## 1. レイアウト要素

### Page / Article

```html
<div class="page shift">
  <article>
    <!-- コンテンツ全体 -->
  </article>
</div>
```

- `.page` は最大幅 `1180px`（TOC展開時は `100vw - 320px`、折りたたみ時は `100vw - 4rem`）に自動調整
- `.shift` は TOC開閉時の左マージン調整用
- `<article>` は白い用紙としてコンテンツ全体を包む

### TOC Toggle ボタンとBackdrop

```html
<button class="toc-toggle is-open" id="toc-toggle" aria-label="目次を開閉" aria-expanded="true">
  <svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
</button>
<div class="toc-backdrop" id="toc-backdrop" aria-hidden="true"></div>
```

- TOC開閉ボタンは左上に固定。TOC展開時はTOC右端に重ねて表示される
- Backdropは狭いビューポート（`max-width:1099px`）でTOCがオーバーレイ表示になったときの背景

---

## 2. タイトルブロック

```html
<header class="title-block">
  <div class="eyebrow">【Category】 · 【Sub Category】</div>
  <h1>【タイトル】</h1>
  <p class="lede">【リード文：全体像を1〜2文で】</p>
  <div class="meta-row">
    <span class="meta-label">Updated</span>
    <span class="meta-value">2026.04</span>
  </div>
  <div class="meta-row">
    <span class="meta-label">Tags</span>
    <div class="chips">
      <span class="chip">tag1</span>
      <span class="chip">tag2</span>
    </div>
  </div>
</header>
```

- `.eyebrow`: JetBrains Monoでカテゴリを示す小さなラベル（大文字・letter-spacing広め）
- `h1`: Source Serif 4、`text-wrap: balance` で改行バランス自動調整
- `.lede`: 導入文。`max-width: 44em` で読みやすい行長
- `.meta-row`: `Updated`（更新日）や `Tags`（タグ）を並べる。`meta-label` は大文字で小さく
- `.chips` > `.chip`: 角丸999px、淡いアクセント色背景のタグ

---

## 3. 左サイドバーTOC

```html
<aside class="toc" id="toc">
  <div class="toc-head">
    <span class="toc-dot"></span>
    <span class="toc-title">Contents</span>
  </div>
  <nav>
    <ol>
      <li><a href="#sec-overview"><span class="num">—</span>概要</a></li>
      <li><a href="#sec-1" class="active"><span class="num">01</span>セクション名</a></li>
      <li><a href="#sec-2"><span class="num">02</span>セクション名</a></li>
      <li><a href="#sec-summary"><span class="num">—</span>Summary</a></li>
    </ol>
  </nav>
  <div class="toc-foot">Category · YYYY.MM</div>
</aside>
```

- `width:260px` 固定。`position:fixed`で画面左に張り付く
- `IntersectionObserver` によりスクロール連動で `.active` がつく項目が切り替わる
- `.num` にはセクション番号（`01`, `02`...）を入れる。概要・Summary は `—` でOK
- アクティブ項目は左側に3px幅の青い縦線が表示される（`::before` で実装）
- 狭いビューポートではオーバーレイモードに切り替わり、Backdropクリックで閉じる
- TOC開閉状態は localStorage に保存される

---

## 4. 概要セクション（Overview）

```html
<section class="ov-section" id="sec-overview">
  <h2 class="ov-h">概要</h2>
  <div class="ov-box">
    <p>トピックの全体像を説明する段落。<strong>重要キーワード</strong> は strong で強調。</p>
    <div class="ov-grid">
      <div class="ov-item">
        <div class="ov-icon">
          <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
        </div>
        <div><h4>ポイント1</h4><p>簡潔な説明</p></div>
      </div>
      <!-- 必要なだけ .ov-item を繰り返す -->
    </div>
  </div>
</section>
```

- `.ov-h` は時計アイコン付きの見出し（`::before` でSVGを埋め込み）。絵文字にしたい場合は `<h2 class="ov-h" data-emoji="📋">` のように `data-emoji` 属性を付ける
- `.ov-box` は淡いグラデーション背景の白いボックス
- `.ov-grid` は `auto-fit minmax(230px, 1fr)` で自動折り返し
- `.ov-item` はホバーで `translateY(-1px)` + 背景色変化
- `.ov-icon` は青グラデーションの正方形（44px）。内部SVGはstroke=1.8推奨
- `.ov-icon.emoji` を付けると薄い青グラデ背景+青枠線になり、絵文字が映える（使用例: `<div class="ov-icon emoji">🎯</div>`）

---

## 5. コンテンツセクション

```html
<section class="ct" id="sec-1">
  <div class="sec-head">
    <div class="sec-icon">
      <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/></svg>
    </div>
    <h2><span class="num">01</span>セクションタイトル</h2>
  </div>
  <p>本文段落。<span class="term">専門用語</span>には .term クラス。</p>
  <h3>サブ見出し</h3>
  <p>...</p>
</section>
```

- `.sec-head` は44pxのアイコン + 番号付き見出し + 下に青い2px線
- `.sec-icon` は薄青背景+青枠線。SVGでも絵文字でもそのまま入る（例: `<div class="sec-icon">🔐</div>`）
- `.num` にはセクション番号を入れる（JetBrains Mono、小さく）
- `h3` は本文フォントで、先頭に `▸` が自動で付く
- `h4` は Inter（サンセリフ）、小見出しとして使う
- `.term` はホバーで背景色がつく専門用語スパン

---

## 6. Callout（情報ボックス）

4種類のバリエーションがある。すべてホバーで左ボーダーが `3px → 5px` に太化する。

### Def（用語定義）— 青

```html
<div class="callout def">
  <div class="icon">Def</div>
  <div class="body">
    <strong>用語名</strong>
    <p>定義文。必要なら <code>コード</code> や <span class="term">他の用語</span> も含められる。</p>
  </div>
</div>
```

### Note（補足・注釈）— グレー

```html
<div class="callout note">
  <div class="icon">Note</div>
  <div class="body">
    <p>補足説明</p>
  </div>
</div>
```

### Warn（注意・警告）— オレンジ

```html
<div class="callout warn">
  <div class="icon">Warn</div>
  <div class="body">
    <strong>警告のタイトル</strong>
    <p>警告内容</p>
  </div>
</div>
```

### Tip（ヒント）— 緑

```html
<div class="callout tip">
  <div class="icon">Tip</div>
  <div class="body">
    <strong>覚え方</strong>
    <p>ヒントや覚え方</p>
  </div>
</div>
```

**使い分けの目安:**

| タイプ | 使う場面 |
|--------|----------|
| `def` | 新しい用語を初出で紹介するとき |
| `note` | 本筋から逸れた補足・注釈 |
| `warn` | 落とし穴・陥りやすい誤解・危険 |
| `tip` | 覚え方・実践のコツ・応用 |

---

## 7. コード・数式

### インラインコード

```html
<p>関数 <code>encrypt()</code> を呼び出すと...</p>
```

- 薄い水色背景、罫線1px、小さめフォント（.88em）
- 色は `--accent-ink` で本文から浮かせる

### コードブロック（複数行）

```html
<pre><span class="lang">python</span><code>def greet(name):
    return f"Hello, {name}!"</code></pre>
```

- `<pre>` が外枠、内部の `<code>` が本文
- `<span class="lang">` は右上のコーナーに言語ラベルを表示（大文字・letter-spacing広め）
- 横に長いコードは `overflow-x: auto` で自動スクロール

**重要な注意:**

- `<pre>` は空白・改行をそのまま表示する。インデントや改行は意図どおりに書く
- `<pre>` 開始タグと最初のコードの間、最後のコードと `</pre>` の間に余分な改行を入れない（上下に無駄な空白行が入る）
- HTMLの特殊文字（`<` `>` `&`）は `&lt;` `&gt;` `&amp;` にエスケープする

### シンタックスハイライト

`<pre>` 内のコードを `<span class="tok-*">` で囲むと手動ハイライトできる。自動パーサは積まない方針（静的HTML単体で完結させるため）。

```html
<pre><span class="lang">javascript</span><code><span class="tok-com">// 配列をフィルタ</span>
<span class="tok-kw">const</span> result = items.<span class="tok-fn">filter</span>(x => x &gt; <span class="tok-num">10</span>);
<span class="tok-fn">console</span>.<span class="tok-fn">log</span>(<span class="tok-str">"found"</span>, result.length);</code></pre>
```

| クラス | 用途 | 色 |
|--------|------|-----|
| `.tok-kw` | キーワード（`if`, `def`, `return`, `const`, `class`） | 紫 |
| `.tok-str` | 文字列リテラル（`"..."`, `'...'`） | 緑 |
| `.tok-num` | 数値リテラル | オレンジ |
| `.tok-com` | コメント | グレー（italic） |
| `.tok-fn` | 関数名・メソッド名 | 青 |

**ハイライトの方針:**

- 全語彙を厳密にハイライトする必要はない。**主要なキーワード・文字列・コメント** を色分けするだけで十分読みやすくなる
- 可読性を下げるなら無理にハイライトしない（短いコマンドライン1行など）
- コメント（`.tok-com`）は最優先でハイライトする — 学習者の目線誘導に効く

### 数式ボックス

```html
<div class="formula">
  <div class="fm">C<sub>i</sub> = E<sub>K</sub>( P<sub>i</sub> ⊕ C<sub>i−1</sub> )</div>
  <div class="cap">暗号化：i番目の平文と直前の暗号文をXORしてから暗号化</div>
</div>
```

- `.fm` は数式本体、JetBrains Monoで中央揃え
- `.cap` は説明（サブ文字サイズ）
- `<sub>` / `<sup>` は添字・指数として使える
- 特殊記号: `⊕`（XOR）、`⊗`（テンソル積）、`∥`（連接）などはUnicodeで直接記述

---

## 8. テーブル・タグ

### 基本テーブル

```html
<table>
  <thead>
    <tr><th>列1</th><th>列2</th><th>列3</th></tr>
  </thead>
  <tbody>
    <tr><td>データ</td><td>データ</td><td><span class="tag tag-ok">OK</span></td></tr>
    <tr><td>データ</td><td>データ</td><td><span class="tag tag-wa">Warning</span></td></tr>
    <tr><td>データ</td><td>データ</td><td><span class="tag tag-ng">NG</span></td></tr>
  </tbody>
</table>
```

- `thead` は太い黒線で挟まれる（学術論文の表スタイル）
- `tbody tr` はホバーで背景が `--bg-subtle` に
- 最終行の下にも太い黒線が入る

### ステータスタグ

| クラス | 用途 | 色 |
|--------|------|-----|
| `.tag.tag-ok` | 正常・OK | 緑 |
| `.tag.tag-wa` | 警告・Warning | オレンジ |
| `.tag.tag-ng` | NG・エラー | 赤 |

---

## 9. リスト

### 通常のunordered list

```html
<ul>
  <li>項目1</li>
  <li>項目2</li>
</ul>
```

- 先頭に `▪` が青で表示される

### Check list（チェックマーク付き）

```html
<ul class="check">
  <li>完了項目1</li>
  <li>完了項目2</li>
</ul>
```

- 先頭に `✓` が緑で表示される

### Ordered list

```html
<ol>
  <li>手順1</li>
  <li>手順2</li>
</ol>
```

- 番号は青色のJetBrains Monoで表示される（`::marker` 使用）

---

## 10. Compare（2カラム比較）

```html
<div class="compare">
  <div class="cc">
    <h4>カテゴリA</h4>
    <ul>
      <li>特徴1</li>
      <li>特徴2</li>
    </ul>
  </div>
  <div class="cc dec">
    <h4>カテゴリB</h4>
    <ul>
      <li>特徴1</li>
      <li>特徴2</li>
    </ul>
  </div>
</div>
```

- `.cc` はデフォルト青（`--info`）の上ボーダー
- `.cc.dec` をつけると緑（`--ok`）の上ボーダーに切り替わる
- 狭い画面では自動で1カラムに折り返す
- 「暗号化 vs 復号」「手動 vs 自動」のような2者比較で使う

---

## 11. Summary（まとめカードグリッド）

```html
<section id="sec-summary" class="summary">
  <div class="summary-head">
    <div class="summary-icon">
      <svg viewBox="0 0 24 24"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>
    </div>
    <div>
      <div class="subt">Key Takeaways</div>
      <h3>まとめ</h3>
    </div>
  </div>
  <div class="summary-grid">
    <div class="summary-item">
      <div class="num">01</div>
      <div class="body">
        <h4>要点のタイトル</h4>
        <p>要点の説明</p>
      </div>
    </div>
    <!-- 必要なだけ .summary-item を繰り返す -->
  </div>
</section>
```

- ページ末尾に配置。グラデーション背景＋青い枠線＋影で特別感を演出
- `.summary-item` は白いカード、ホバーで浮き上がる
- `.num` は円形の番号バッジ（30px、青）
- `.summary-icon.emoji` を付けると薄い青グラデ背景に絵文字が映える仕上がりになる（使用例: `<div class="summary-icon emoji">✨</div>`）

---

## 12. プログレスバー

```html
<div class="progress" id="progress"></div>
```

- `position:fixed; top:0` で画面上端に張り付く2px幅のバー
- スクロール量に応じて幅が `0%` → `100%` に変化
- JSで `window.addEventListener('scroll', updateProgress)` して幅を更新する（テンプレートに実装済み）

---

## 13. アイコン（絵文字優先、必要時にSVG）

テンプレには4箇所のアイコンボックスがある。**絵文字を使うのが基本**で、SVGは必要なときだけ使う。

### なぜ絵文字優先か

- SVG を自力で書くのは負担が大きい（`viewBox` や `path` を考える必要がある）
- トピックに合わないSVGになりやすい（「ステートレス」に波線など、意味的にズレる図形を書きがち）
- 絵文字なら1文字で意味が伝わる（🔐 = 暗号、📡 = 通信、⚖️ = 比較）
- 絵文字はOS標準の高品質レンダリングが得られる

### 対応箇所の一覧

| 場所 | 絵文字版（推奨） | SVG版（必要時） |
|------|----------------|----------------|
| `.sec-icon` | `<div class="sec-icon">🔐</div>` | `<div class="sec-icon"><svg>...</svg></div>` |
| `.ov-h::before` | `<h2 class="ov-h" data-emoji="📋">概要</h2>` | `<h2 class="ov-h">概要</h2>`（属性なしでSVG時計がデフォルト） |
| `.ov-icon` | `<div class="ov-icon emoji">🎯</div>` | `<div class="ov-icon"><svg>...</svg></div>` |
| `.summary-icon` | `<div class="summary-icon emoji">✨</div>` | `<div class="summary-icon"><svg>...</svg></div>` |

### `.ov-h`（概要見出し）の例外

`.ov-h` は他のアイコンとは異なり、**デフォルトのSVG時計をそのまま使うのが基本**。理由:

- 概要見出しは「概要」というラベル固定なので、時計アイコンがトピックを問わず意味的に通じる
- デフォルトで時計SVGが埋め込み済みのため、何も書かなくてよい
- 毎回 `data-emoji` を考えるより、そのままの方が楽

絵文字にしたいケース（📋・🔍・🎯など、より内容に合う絵文字が見つかった場合）だけ、`data-emoji` 属性を追加する。

### 修飾子 `.emoji` の必要性

- **`.sec-icon`** と **`.ov-h`**: 元々が薄青背景なので修飾子は不要。中身に絵文字を置くだけでOK
- **`.ov-icon`** と **`.summary-icon`**: 元々が濃い青グラデ背景なので、絵文字を入れるだけだと色が潰れる。**必ず `.emoji` 修飾子を付ける**。これで薄い青グラデ背景に切り替わる

### SVGを選ぶべき場面

絵文字を基本としつつ、以下のような場合はSVGを使う:

- **専門的な処理フロー内の小アイコン**: 暗号プロトコルの状態遷移、アルゴリズムの特殊ステップなど、絵文字では表現できない図
- **格調高いトーンの教材**: 学術論文風、フォーマルな技術書風などでカラー絵文字が浮いてしまう場合
- **意味的に中立な抽象図形が欲しい**: 円・矩形・線の組み合わせなど、特定の意味を持たせたくない場合

### 1ドキュメント内での混在

絵文字とSVGを混ぜても破綻しない。ただし統一感が欲しければ全部絵文字で揃えるのが無難。もし混ぜるなら「概要ov-itemは絵文字、フロー図内の補助アイコンはSVG」のような**用途の違いで切り分ける**。

### `.emoji` 修飾子のスタイル仕様

```css
/* 薄い青グラデ + 青枠線 + 青文字（.ov-icon と .summary-icon 共通） */
.ov-icon.emoji,
.summary-icon.emoji {
  background: linear-gradient(135deg, #fff 0%, var(--accent-soft) 100%);
  border: 1.5px solid var(--accent);
  color: var(--accent);
  font-size: 1.4rem;  /* 絵文字サイズ */
}
```

### 絵文字の選び方ガイド

用途別の例。コンテンツのテーマに合わせて選ぶ。

| テーマ | 絵文字の例 |
|--------|-----------|
| セキュリティ・暗号 | 🔐 🔒 🔑 🛡️ |
| データ・分析 | 📊 📈 📉 📑 |
| システム・設定 | ⚙️ 🔧 🖥️ 💾 |
| 警告・注意 | ⚠️ 🚨 ❗ |
| 成功・完了・目標 | ✅ 🎉 ✨ 🎯 |
| 学習・理解 | 💡 📖 📝 🎓 |
| 時間・プロセス | 🕐 ⏱️ 🔄 ➡️ |
| 判断・比較 | ⚖️ 🤔 🔍 |
| 通信・ネットワーク | 📡 🌐 📨 |
| 構造・部品 | 🧩 📦 🏗️ |

### 選ぶコツ

- **1ドキュメントに同じ絵文字を繰り返さない**: 各セクションに違う絵文字を充てると視覚的な目印になる
- **セマンティックな絵文字を選ぶ**: 「暗号化の章だから🔐」のように、概念と直接結びつく絵文字を選ぶ。「なんとなく派手そうだから🎊」のような選び方は避ける
- **複雑すぎる絵文字は避ける**: 44px の箱に収まったときに視認できるかを基準にする。細かすぎる絵文字（🏢🗿🗻など）は小さく見えにくい

---

## インタラクション一覧

学習を補助する範囲に絞ったインタラクション。すべて `prefers-reduced-motion: reduce` 時に無効化される。

| 対象 | 効果 | CSS |
|------|------|-----|
| `.ov-item` | 浮き上がり + 背景色 | `transition:background-color .2s, transform .2s` |
| `.callout` | 浮き上がり + 影 | `transition:transform .25s cubic-bezier(.4,0,.2,1), box-shadow .25s cubic-bezier(.4,0,.2,1)` |
| `.term` | 背景色 + 下線実線化 | `transition:background-color .2s, border-bottom-style .2s` |
| `.summary-item` | 浮き上がり + 影 + 枠線色 | `transition:transform .15s, box-shadow .15s, border-color .15s` |
| `.toc a` | 色・背景色遷移 | `transition:color .2s, background-color .2s` |
| `tbody tr` | 背景色変化 | `transition:background-color .15s` |
