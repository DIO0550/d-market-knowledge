---
name: html-educational-material
description: 技術教育・解説資料用のHTML作成スキル。暗号技術、アルゴリズム、システム設計などの技術概念を図解・フロー図・比較表を使って視覚的に説明するHTML資料を作成する際に使用。学術ノート風ライトテーマのモダンなデザイン、左サイドバー目次（スクロール連動）、CSSグリッドによる正確な配置、プロフェッショナルな質感、アクセシビリティ対応（prefers-reduced-motion）を特徴とする。解説HTML作成後は理解度確認用のクイズHTMLも別ファイルとして生成可能（4択・YES/NO・並べ替えの3形式、即時フィードバック付き）。「教育用HTML」「解説資料」「技術ドキュメント」「図解付きHTML」「学習ノート」「理解度クイズ」「並べ替え問題」の作成時にトリガー。
---

# HTML Educational Material Design System

技術教育・解説資料向けのHTML作成ガイド。学術ノート風ライトテーマをベースに、読みやすさと正確な視覚表現を両立する。

## クイックスタート

1. `assets/template.html` をコピーして解説HTMLを作成
2. 詳細なコンポーネントは `references/components.md` を参照
3. フロー図を描く場合は `references/flow-diagrams.md` を参照
4. （オプション）`assets/quiz-template.html` をコピーしてクイズHTMLを作成
5. クイズ設計の詳細は `references/quiz-components.md` を参照

## ファイル命名規則

- **解説HTML**: `<title>` の内容をファイル名に使用（例: `<title>CBCモード解説</title>` → `CBCモード解説.html`）
- **クイズHTML**: `{解説HTMLのタイトル}_クイズ.html`（例: `CBCモード解説_クイズ.html`）
- 解説HTML・クイズHTMLは相互リンクさせる（クイズ側の `back-link` と、結果画面の「解説を見る」ボタン）

## デザインコンセプト

学術論文・技術ノートの静謐さをベースに、必要な箇所にだけインタラクションを織り込む。派手な演出を避け、コンテンツの可読性を最優先する。

- **タイポグラフィ**: 本文はセリフ体（Source Serif 4 + Noto Serif JP）、UI・コードはサンセリフ/モノスペース（Inter + JetBrains Mono）
- **カラー**: 柔らかな青（#2c5aa0）を主軸に、情報・警告・OK・危険をセマンティック色で区別
- **レイアウト**: 左固定TOC（260px）+ 本文（最大1180px）。狭い画面ではTOCがオーバーレイ化
- **質感**: 白基調の用紙感、控えめな罫線、微かな影

## 基本構造

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タイトル</title>
    <!-- フォント: Source Serif 4, Inter, JetBrains Mono, Noto Serif JP, Noto Sans JP -->
    <style>/* CSS変数とスタイル */</style>
</head>
<body>
    <div class="progress" id="progress"></div>
    <button class="toc-toggle is-open" id="toc-toggle">...</button>
    <div class="toc-backdrop" id="toc-backdrop"></div>
    <aside class="toc" id="toc">...</aside>
    <div class="page shift">
        <article>
            <header class="title-block">...</header>
            <section class="ov-section" id="sec-overview">...</section>
            <section class="ct" id="sec-1">...</section>
            ...
            <section id="sec-summary" class="summary">...</section>
        </article>
    </div>
    <script>/* TOC・プログレスバー・スクロール連動 */</script>
</body>
</html>
```

## CSS変数（カラースキーム）

```css
:root{
    /* 背景 */
    --bg-page:#f4f7fb;
    --bg-surface:#ffffff;
    --bg-subtle:#eaf0f7;
    /* テキスト */
    --ink-primary:#1a2332;
    --ink-secondary:#3e4a5e;
    --ink-muted:#6b7a8f;
    /* 罫線 */
    --rule:#cfd9e6;
    --rule-strong:#a8b5c7;
    /* アクセント（プライマリ：青） */
    --accent:#2c5aa0;
    --accent-2:#4a7ec4;
    --accent-soft:#dde8f5;
    --accent-ink:#1e3f73;
    /* セマンティック色 */
    --info:#2c5aa0;   --info-soft:#dde8f5;
    --warn:#a06a1c;   --warn-soft:#faecd0;
    --ok:#2d7a5f;     --ok-soft:#d8ebe2;
    --danger:#a33a3a; --danger-soft:#f5dede; --danger-ink:#7a2828;
    /* コード */
    --code-bg:#eef3f9;
}
```

**色の使い分け原則:**

| 概念 | CSS変数 | 用途 |
|------|---------|------|
| プライマリアクション | `--accent` | 見出し下線、TOC強調、リンク |
| 情報・解説 | `--info` / `--info-soft` | `.callout.def`、フロー図の処理ブロック（Eₖ, Dₖ） |
| 注意・警告 | `--warn` / `--warn-soft` | `.callout.warn`、暗号文ブロック |
| 正常・成功 | `--ok` / `--ok-soft` | `.callout.tip`、平文ブロック、check list |
| 危険・失敗 | `--danger` / `--danger-soft` | エラー状態、不正解 |

## 主要コンポーネント

詳細は [references/components.md](references/components.md) を参照。

### 構造要素

- `.toc` - 左サイドバー目次（折りたたみ可・スクロール連動ハイライト）
- `.title-block` - タイトル・リード文・メタ情報
- `.ov-section` + `.ov-box` - 概要セクション
- `section.ct` - 通常のコンテンツセクション（`.sec-head` + 本文）
- `.summary` - まとめセクション（カードグリッド付き）

### Callout（情報ボックス）

| クラス | 用途 | 色 |
|--------|------|-----|
| `.callout.def` | 用語定義 | 青 |
| `.callout.note` | 補足・注釈 | グレー |
| `.callout.warn` | 注意・警告 | オレンジ |
| `.callout.tip` | ヒント・Tips | 緑 |

### フロー図ブロック

| クラス | 用途 | 色 |
|--------|------|-----|
| `.block.b-plain` | 平文・入力 | 緑 |
| `.block.b-cipher` | 暗号文・出力 | オレンジ |
| `.block.b-enc`, `.block.b-dec` | 暗号化・復号処理 | 青 |
| `.block.b-iv` | 初期値 | 紺 |
| `.block.b-xor` | XOR演算（丸形） | グレー |

### エラー状態修飾子

| クラス | 用途 |
|--------|------|
| `.b-err` | 完全破壊（赤） |
| `.b-partial` | 部分的影響（オレンジ） |
| `.b-ok` | 正常（緑） |

### テキスト装飾

- `.term` - 専門用語（下線ドット、ホバーで背景色）
- `<em>` - 蛍光ペン風マーカー
- `<strong>` - 強調（濃い文字色）
- `<code>` - インラインコード
- `<pre><span class="lang">言語名</span><code>...</code></pre>` - 複数行コードブロック（右上に言語ラベル）

### シンタックスハイライト用トークンクラス

`<pre>` 内で `<span class="tok-*">` で囲むことで手動ハイライトが可能。

| クラス | 用途 | 色 |
|--------|------|-----|
| `.tok-kw` | キーワード（if, def, return など） | 紫 |
| `.tok-str` | 文字列リテラル | 緑 |
| `.tok-num` | 数値リテラル | オレンジ |
| `.tok-com` | コメント | グレー（italic） |
| `.tok-fn` | 関数名 | 青 |

### アイコン（絵文字優先、必要時にSVG）

**アイコンは絵文字を基本とする。** SVGを自力で書くのは負担が大きく、トピックに合わない図形になりやすい。絵文字なら一文字で意味が伝わる。

| 場所 | 絵文字版（推奨） | SVG版（必要時） |
|------|-----------------|----------------|
| `.sec-icon` | `<div class="sec-icon">🔐</div>` | `<div class="sec-icon"><svg>...</svg></div>` |
| `.ov-icon` | `<div class="ov-icon emoji">🎯</div>` | `<div class="ov-icon"><svg>...</svg></div>` |
| `.summary-icon` | `<div class="summary-icon emoji">✨</div>` | `<div class="summary-icon"><svg>...</svg></div>` |
| `.ov-h::before` | `<h2 class="ov-h" data-emoji="📋">` | `<h2 class="ov-h">`（デフォルトで時計SVG） |

**`.ov-h`（概要見出し）の例外:** 概要見出しは「概要」というラベル固定なので、デフォルトのSVG時計がそのまま意味的に適切。通常は `<h2 class="ov-h">概要</h2>` のままでよく、あえて絵文字を設定する必要はない。トピックに合う絵文字（📋・🔍・🎯など）を使いたい場合だけ `data-emoji` 属性を追加する。

**重要:** `.ov-icon` や `.summary-icon` で絵文字を使うときは必ず `.emoji` 修飾子クラスを付ける。付けないと濃い青グラデ背景に絵文字が載り、色が潰れる。

**SVGを選ぶのは以下のような場合のみ:**

- 暗号・プロトコル処理フロー内の小アイコンなど、絵文字では表現できない専門的な図
- カラー絵文字だとコンテンツのトーンから浮くような、格調高い教材
- 意味的に中立な抽象図形（円・線・矩形など）を使いたい場合

絵文字とSVGを1つのドキュメント内で混在させても構わないが、統一感を優先するなら全部絵文字で揃えるのが無難。

### 絵文字選びのガイド

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

## フロー図の組み方

詳細は [references/flow-diagrams.md](references/flow-diagrams.md) を参照。

```css
.flow{display:flex;flex-direction:column;gap:.4rem;min-width:820px}
.frow{
    display:grid;
    grid-template-columns:68px 110px 36px 110px 36px 110px 36px 110px;
    align-items:center;justify-items:center;gap:.3rem;
}
```

`.frow` は「ラベル + ブロック + 矢印 + ブロック + 矢印 + ...」のパターン。縦方向の整列を保つため、全行で同じ列構成を維持する。

## インタラクション設計

不要な派手さを避け、学習を補助する方向に絞る。全てのインタラクションは `prefers-reduced-motion: reduce` 時に無効化される。

**解説HTML側:**

1. `.ov-item` ホバー：背景色変化 + 微小な浮き上がり
2. `.callout` ホバー：浮き上がり + 影（クリーンな持ち上がり感）
3. `.term` ホバー：背景色がつく + 下線が実線化
4. `.summary-item` ホバー：浮き上がり + 影 + ボーダー色変化
5. TOC項目のアクティブ切替：滑らかなテキスト色遷移

**クイズHTML側:**

1. `.option` ホバー：`translateX(2px)` で右にスライド
2. 正誤判定時：カードが一瞬フラッシュ（`flash-correct` / `flash-incorrect` アニメ）
3. `.sort-item.dragging`：微回転 + スケール + 影（ドラッグ物理感）
4. 結果画面のスコア数字：0から正解数までカウントアップ（800ms）

## デザイン原則

1. **縦方向の整列**: フロー図はCSSグリッドで列幅を固定
2. **色の一貫性**: 同じ概念には同じセマンティック色を使用
3. **階層的なコントラスト**: `--bg-page` → `--bg-surface` → `--bg-subtle` の順で用紙感を演出
4. **静けさを保つ**: スクロールインアニメなどコンテンツの表示を遅らせる演出は使わない
5. **アクセシビリティ**: `prefers-reduced-motion` を尊重、十分なコントラスト比を確保

## 推奨フォント

- 本文: `'Source Serif 4', 'Noto Serif JP', Georgia, serif`
- UI・見出し補助: `'Inter', 'Noto Sans JP', sans-serif`
- コード・数式・ラベル: `'JetBrains Mono', monospace`

## クイズHTML生成

解説HTML作成後、理解度確認用のクイズHTMLを別ファイルとして作成する。詳細は [references/quiz-components.md](references/quiz-components.md) を参照。

### 特徴

- **1画面全問表示**: 全問を1ページにまとめて表示
- **即時フィードバック**: 選択時にその場で正誤と解説を表示
- **回答済み数の表示**: ヘッダーに進捗を表示
- **結果画面**: 全問回答後に正答率・問題タイプ別breakdown・評価メッセージを表示
- **リトライ機能**: もう一度挑戦ボタン（回答・シャッフルともにリセット）

### 問題タイプ（この3種類のみ使用可）

**`multiple` / `yesno` / `sort` の3タイプだけが実装されている。** 他のタイプ名（`rank`, `order`, `ranking`, `sequence`, `reorder` など）は**使用不可** — テンプレのロジックが対応しておらず、正解判定も不正解時の正解表示も動作しない。

| タイプ | 形式 | 使用場面 |
|--------|------|----------|
| `multiple` | 4択（A/B/C/D） | 概念理解、比較、応用 |
| `yesno` | 2択（YES/NO） | 事実確認、誤解訂正 |
| `sort` | 並べ替え（ドラッグ＆ドロップ） | 手順・プロセス、時系列、重要度・優先度の序列 |

**sort型を使うべき問題の例:**

- 暗号化・復号の処理ステップを正しい順に並べる
- アルゴリズムの実行フェーズを順番に並べる
- エラー影響度・重要度の高い順に並べる
- プロトコルハンドシェイクのメッセージ順序

**sort型を使うべきでない例:**

- 単なる事実の選択（→ `multiple` を使う）
- 二者択一の判断（→ `yesno` を使う）
- 順序に意味がない並列的な要素の列挙

### クイズデータ形式（厳守すべきルール）

**重要な制約:**

- **タイプ名は `'multiple'` / `'yesno'` / `'sort'` のいずれか**。他の名前（例: `'rank'`）を使ってはいけない
- **`sort` の `items` は必ず文字列の配列**。オブジェクト（例: `{id: 'a', text: '...'}`）を使ってはいけない
- **`sort` に `correct` や `correct_order` プロパティを書いてはいけない**。`items` の定義順がそのまま正解判定の基準になる（表示時は自動シャッフル）

```javascript
const quizData = [
    {
        type: 'multiple',
        question: '問題文',
        options: ['選択肢A', '選択肢B', '選択肢C', '選択肢D'],
        correct: 0, // 正解のindex（0始まり）
        explanation: '解説テキスト'
    },
    {
        type: 'yesno',
        question: 'YES/NO問題文',
        correct: 'yes', // または 'no'
        explanation: '解説テキスト'
    },
    {
        type: 'sort',
        question: '並べ替え問題文',
        items: [
            'ステップ1（正解順で記述）',
            'ステップ2（正解順で記述）',
            'ステップ3（正解順で記述）'
        ],
        // items は「正解の順序」で定義する。ユーザーには表示時に自動でシャッフルされる。
        // correct プロパティは不要（itemsの順序そのものが正解）。
        explanation: '解説テキスト'
    }
];
```

**❌ よくある間違いと正しい書き方:**

```javascript
// ❌ 間違い: type が 'rank'、items がオブジェクト、correct_order を使用
{
    type: 'rank',                    // → 'sort' に
    items: [
        { id: 'a', text: '項目A' },  // → 文字列だけに
        { id: 'b', text: '項目B' }
    ],
    correct_order: ['a', 'b']        // → プロパティごと削除
}

// ✅ 正しい書き方
{
    type: 'sort',
    items: [
        '項目A（正解順で1番目）',
        '項目B（正解順で2番目）'
    ],
    explanation: '...'
}
```

### クイズ生成ワークフロー

1. 解説HTMLを作成
2. 主要なトピックから5〜10問を選定（各問題タイプのバランスを意識）
3. `assets/quiz-template.html` をコピー
4. `quizData` 配列に問題を記述
5. ヘッダーの `back-link` と結果画面の「解説を見る」ボタンのhrefを解説HTMLのファイル名に更新
6. `subtitle` と `title` を解説HTMLに合わせて更新
7. ファイル名を `{解説HTMLのタイトル}_クイズ.html` にする
