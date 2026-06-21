# クイズコンポーネントリファレンス

理解度確認用クイズHTMLのコンポーネント集。学術ノート風ライトテーマをベースに、3つの問題タイプ（`multiple` / `yesno` / `sort`）を1画面全問表示形式で提供する。

## 目次

1. [全体構造](#1-全体構造)
2. [問題タイプの選び方](#2-問題タイプの選び方)
3. [クイズデータ形式](#3-クイズデータ形式)
4. [問題カード（Question Card）](#4-問題カードquestion-card)
5. [4択問題（multiple）](#5-4択問題multiple)
6. [YES/NO問題（yesno）](#6-yesno問題yesno)
7. [並べ替え問題（sort）](#7-並べ替え問題sort)
8. [フィードバック表示](#8-フィードバック表示)
9. [結果画面](#9-結果画面)
10. [インタラクション仕様](#10-インタラクション仕様)
11. [良い問題を作るためのガイド](#11-良い問題を作るためのガイド)

---

## 1. 全体構造

```html
<body>
  <div class="progress" id="progress"></div>
  <div class="container">
    <header>
      <a class="back-link" href="解説HTMLファイル名.html">Back to notes</a>
      <div class="eyebrow">Self-Check Quiz</div>
      <h1>理解度チェック</h1>
      <p class="subtitle">元資料タイトル · 全N問</p>
      <div class="score-display">
        <span class="score-label">ANSWERED</span>
        <span class="score-value" id="answered-count">0</span>
        <span class="score-label">/ <span id="total-count">0</span></span>
      </div>
    </header>
    <main id="quiz-container"></main>
    <div class="submit-section" id="submit-section">
      <button class="submit-btn" id="submit-btn" onclick="showResults()" disabled>結果を見る</button>
      <p class="submit-hint" id="submit-hint">すべての問題に回答してください</p>
    </div>
    <div class="result-section" id="result-section">
      <!-- JSで動的に内容を描画 -->
    </div>
  </div>
  <button class="scroll-top-btn" id="scroll-top-btn" onclick="scrollToTop()">↑</button>
  <script>/* quizData と 全ロジック */</script>
</body>
```

- 最大幅 `780px` 中央寄せ。解説HTMLより狭い（回答に集中させる）
- 問題カードはJS（`renderAll()`）で動的に描画される
- `back-link` と結果画面の「解説を見る」ボタンは、対応する解説HTMLへのリンクを設定する

---

## 2. 問題タイプの選び方

| タイプ | 向いているテーマ |
|--------|------------------|
| `multiple`（4択） | 概念理解、比較、応用判断、選択肢の中から最適を選ぶ問題 |
| `yesno`（2択） | 事実確認、誤解の訂正、「これは正しい？」という問い |
| `sort`（並べ替え） | 手順・プロセスの順序、時系列、重要度・優先度の序列 |

**sort型を使うべき場面の例:**

- 暗号化・復号の処理ステップを正しい順に並べる
- プロトコルハンドシェイクのメッセージ順序
- アルゴリズムのフェーズ（初期化 → 計算 → 検証 → 終了）
- 影響度・緊急度の高い順
- 歴史的な技術の登場順

**sort型を使うべきでない場面の例:**

- 順序に意味がない並列的な要素の列挙（→ `multiple` で「該当するものを選べ」にする）
- 単一の事実の選択（→ `multiple` または `yesno`）
- 2つのどちらかを選ぶ判断（→ `yesno`）

### バランスの目安

全体で5〜10問を基本とする。3タイプを混ぜるのが理想だが、教材のテーマによっては偏ってもよい。

- 概念系の教材: `multiple` 60% + `yesno` 30% + `sort` 10%
- 手順系の教材: `sort` 40% + `multiple` 40% + `yesno` 20%
- 事実確認系: `yesno` 50% + `multiple` 50%

---

## 3. クイズデータ形式

`quizData` 配列に問題を順に記述する。

### ⚠️ 厳守すべきルール（違反すると正解判定が動かない）

クイズテンプレートには **`multiple` / `yesno` / `sort` の3タイプだけ** が実装されている。以下のルールを必ず守ること:

1. **`type` には `'multiple'` / `'yesno'` / `'sort'` のいずれかのみ使う**
   - 違反例: `'rank'`, `'order'`, `'ranking'`, `'sequence'`, `'reorder'` → **どれも実装されていないため動かない**
   - 並べ替え問題は **必ず `'sort'`** と書く

2. **`sort` の `items` は必ず文字列の配列にする**
   - 違反例: `items: [{id: 'a', text: '項目A'}, {id: 'b', text: '項目B'}]` → オブジェクト形式は非対応
   - 正しい形式: `items: ['項目A', '項目B']` （文字列だけの配列）

3. **`sort` に `correct` や `correct_order` プロパティを書かない**
   - `items` の **配列順そのもの** が正解。別途正解を指定するプロパティは存在しない
   - 表示時はコード側が自動でシャッフルするので、ユーザーが見る順序と定義時の順序は別物

### 正しい書き方

```javascript
const quizData = [
  // 4択
  {
    type: 'multiple',
    question: '問題文',
    options: ['選択肢A', '選択肢B', '選択肢C', '選択肢D'],
    correct: 0,  // 正解のindex（0〜3）
    explanation: '解説文'
  },
  // YES/NO
  {
    type: 'yesno',
    question: 'YES/NO問題文',
    correct: 'yes',  // 'yes' または 'no'
    explanation: '解説文'
  },
  // 並べ替え
  {
    type: 'sort',
    question: '並べ替え問題文',
    items: [
      'ステップ1',  // 正解の順序で記述する
      'ステップ2',  // 表示時に自動でシャッフルされる
      'ステップ3',
      'ステップ4'
    ],
    // correct プロパティは不要（itemsの順序そのものが正解）
    explanation: '解説文'
  }
];
```

### ❌ よくある間違いパターン

**パターン1: `type: 'rank'` と書いてしまう**

```javascript
// ❌ 間違い
{ type: 'rank', ... }

// ✅ 正しい
{ type: 'sort', ... }
```

→ `'rank'` はテンプレのロジックで処理されない。`renderSort()` も `submitSort()` も呼ばれず、問題カードが空のまま表示される。

**パターン2: `items` を `{id, text}` オブジェクトで書いてしまう**

```javascript
// ❌ 間違い
{
  type: 'sort',
  items: [
    { id: 'a', text: '項目A' },
    { id: 'b', text: '項目B' }
  ],
  correct_order: ['b', 'a']
}

// ✅ 正しい
{
  type: 'sort',
  items: [
    '項目B（正解順で1番目）',
    '項目A（正解順で2番目）'
  ]
}
```

→ テンプレは `q.items[origIdx]` で文字列として直接表示するため、オブジェクトだと `[object Object]` が表示されてしまう。

**パターン3: `sort` に `correct` を追加してしまう**

```javascript
// ❌ 間違い（4択と混同している）
{
  type: 'sort',
  items: ['A', 'B', 'C'],
  correct: [0, 1, 2]  // このプロパティは読まれない
}

// ✅ 正しい
{
  type: 'sort',
  items: ['A', 'B', 'C']  // この順序が正解
}
```

→ テンプレの正解判定は `sortOrders[idx].every((v,p) => v===p)` で、シャッフル前の `q.items` の並びが基準。別途 `correct` プロパティを用意しても無視される。

### sort型の項目数目安

- **3〜6個** が適切
- 2個だと `yesno` で足りる
- 7個以上だとドラッグ操作が煩雑になる

---

## 4. 問題カード（Question Card）

各問題は `.question-card` で囲まれる。

```html
<div class="question-card" id="question-0">
  <div class="question-header">
    <div class="question-number">Q01</div>
    <span class="question-type">MULTIPLE CHOICE</span>
  </div>
  <p class="question-text">問題文</p>
  <div id="body-0"><!-- 問題タイプごとの本体 --></div>
  <div class="feedback" id="feedback-0"><!-- 正誤フィードバック --></div>
</div>
```

**回答後の状態:**

- 正解時: `.question-card.correct-answered` が付与 → 緑の左ボーダー + `flash-correct` アニメーション
- 不正解時: `.question-card.incorrect-answered` が付与 → 赤の左ボーダー + `flash-incorrect` アニメーション

**質問タイプの表示ラベル:**

| 内部値 | 表示 |
|--------|------|
| `multiple` | `MULTIPLE CHOICE` |
| `yesno` | `YES/NO` |
| `sort` | `SORT` |

---

## 5. 4択問題（multiple）

```html
<div class="options-container" id="options-0">
  <button class="option" data-index="0" onclick="selectAnswer(0,0)">
    <span class="option-label">A</span>
    <span class="option-text">選択肢A</span>
  </button>
  <button class="option" data-index="1" onclick="selectAnswer(0,1)">
    <span class="option-label">B</span>
    <span class="option-text">選択肢B</span>
  </button>
  <!-- C, D も同様 -->
</div>
```

- ホバー時: `translateX(2px)` で右にスライド + 背景色 `--accent-soft`
- 正解選択時: 緑背景 + 緑ラベル
- 不正解選択時: 赤背景 + 赤ラベル、**さらに正解選択肢も緑で表示**（回答後の学習のため）
- 他の選択肢は `.disabled` が付き薄くなる

---

## 6. YES/NO問題（yesno）

```html
<div class="options-container yesno" id="options-0">
  <button class="option yesno-option" data-value="yes" onclick="selectAnswer(0,'yes')">
    <span class="yesno-icon">○</span>
    <span class="option-text">はい (YES)</span>
  </button>
  <button class="option yesno-option" data-value="no" onclick="selectAnswer(0,'no')">
    <span class="yesno-icon">×</span>
    <span class="option-text">いいえ (NO)</span>
  </button>
</div>
```

- 通常は横並び（`flex-direction: row`）
- モバイル（max-width:480px）では縦並びに自動切替
- `○` のアイコン色は緑、`×` は青（ラベルの意味に中立的に対応）

---

## 7. 並べ替え問題（sort）

### レンダリング構造

```html
<div class="sort-header">
  <span>DRAG TO REORDER</span>
  <button class="shuffle-btn" onclick="shuffleSort(0)">shuffle</button>
</div>

<div class="sort-list" id="sort-list-0">
  <div class="sort-item" draggable="true" data-pos="0" data-qi="0">
    <div class="sort-num">1</div>
    <div>ステップの内容</div>
    <div class="sort-handle">⋮⋮</div>
  </div>
  <!-- 各アイテム -->
</div>

<div class="sort-submit">
  <button onclick="submitSort(0)">この順で回答する</button>
</div>
```

### インタラクション仕様

- **ドラッグ操作**: HTML5 Drag&Dropで並べ替え
- **タッチ対応**: モバイル用に `touchstart`/`touchmove`/`touchend` でも同等の挙動
- **ドロップインジケータ**: ドラッグ中のアイテムに `.drop-before` または `.drop-after` を付与し、青い細線で挿入位置を表示
- **shuffleボタン**: 現在の配置を再シャッフル（回答前のみ有効）
- **ドラッグ中の視覚効果**: `.dragging` が付くと `opacity:.55` + `rotate(.5deg) scale(1.02)` + 影、物理的な持ち上げ感
- **この順で回答する**ボタンをクリックで回答確定

### 回答後の表示

**正解の場合:**

```html
<div class="sort-item locked correct">
  <div class="sort-num">1</div>
  <div>ステップ1</div>
  <div class="sort-handle">⋮⋮</div>
</div>
<!-- 全アイテムが緑（.correct） -->
```

**不正解の場合:**

- ユーザーが並べたアイテムに `.locked .wrong` が付く（赤表示）
- その下に `.sort-correct-ref` ブロックが追加され、**正解の順序** が緑で表示される

```html
<div class="sort-correct-ref">
  <div class="sort-correct-ref-head">正解の順序</div>
  <div class="sort-ref-list">
    <div class="sort-ref-item">
      <div class="sort-ref-num">1</div>
      <div>正解順のステップ1</div>
    </div>
    <!-- 以下、正解の順で全アイテム -->
  </div>
</div>
```

### 設計の意図

- **全体正解のみを正解とする**: 途中まで合っていても、全体が揃っていなければ不正解。部分点は与えない（並べ替えは全体の論理を問うものだから）
- **不正解時は正解順を明示**: 単に「間違い」だけでなく、正しい順序を見せることで学習機会にする
- **シャッフル機能**: 回答前なら何度でも並べ直せる。開始配置が気に入らないときのやり直し用

---

## 8. フィードバック表示

全ての問題タイプで共通のフィードバック欄を使う。

```html
<div class="feedback" id="feedback-0">
  <div class="feedback-icon"></div>
  <div class="feedback-content">
    <div class="feedback-title">正解</div>
    <p class="feedback-explanation">解説テキスト</p>
  </div>
</div>
```

- 回答前は非表示（`display: none`）
- 回答時に `.show` が付与され `.correct` または `.incorrect` クラスでスタイル切替
- `fadeIn` アニメーションで自然に登場
- タイトルは自動設定：正解 → "正解"、不正解 → "不正解"

---

## 9. 結果画面

```html
<div class="result-section" id="result-section">
  <div class="result-eyebrow">Final Score</div>
  <h2 class="result-title" id="result-title">お疲れさまでした</h2>
  <div class="result-score">
    <span class="score-number" id="final-score">0</span>
    <span class="score-divider">/</span>
    <span class="score-total" id="result-total">0</span>
  </div>
  <p class="result-percentage" id="result-percentage">正答率: 0%</p>
  <div class="result-breakdown" id="result-breakdown">
    <!-- JSで動的生成 -->
  </div>
  <p class="result-message" id="result-message"></p>
  <div class="result-actions">
    <button class="btn btn-primary" onclick="retryQuiz()">もう一度挑戦</button>
    <a class="btn btn-ghost" href="解説HTMLファイル名.html">解説を見る</a>
  </div>
</div>
```

### 表示内容

1. **スコア**: 0から正解数までカウントアップ（800ms、easeOutQuad）
2. **正答率**: 100分率で表示
3. **breakdown**: 問題タイプごとの正答数。**実際に出題された問題タイプのみ動的に生成される**（全タイプを使っていなくても破綻しない）
4. **評価メッセージ**: 得点率に応じた4段階のテキスト
   - 100%: 「完璧!」
   - 80-99%: 「よく理解できています」
   - 60-79%: 「基本はOK」
   - 0-59%: 「要復習」

### breakdown の動的生成

```javascript
function countByType(){
  const counts={multiple:0, yesno:0, sort:0};
  quizData.forEach(q=>{ counts[q.type]++; });
  return counts;
}
```

出題されていないタイプは `.bd` カードが生成されない。例えば `sort` を使わないクイズでは「並べ替え」欄が結果画面に出ない。

### リトライ

`retryQuiz()` を呼ぶと:

- `answers` 配列をクリア
- `sortOrders` を再シャッフル
- 全問題カードを再描画（回答状態・フィードバック・正誤クラスがクリア）
- ページ最上部へスクロール

---

## 10. インタラクション仕様

すべて `prefers-reduced-motion: reduce` 時に無効化される（グローバルCSSで一括対応）。

| 要素 | 効果 | 実装 |
|------|------|------|
| `.option` hover | 右に2pxスライド + 背景色 | `transition:transform .15s, background-color .15s` |
| 正誤判定時 | カード全体がフラッシュ（0.6s） | `@keyframes flash-correct` / `flash-incorrect` |
| `.sort-item.dragging` | 微回転 + スケール + 影 | `transform:rotate(.5deg) scale(1.02)` |
| `.sort-item` drop indicator | 上下に青い細線 | `box-shadow:0 -2px 0 var(--accent)` / `0 2px 0 var(--accent)` |
| 結果画面スコア | 0→正解数へカウントアップ | `requestAnimationFrame` + easeOutQuad |
| `.feedback` 出現 | フェードイン + 下から8pxスライド | `@keyframes fadeIn` |
| `.result-section` 出現 | 同上 | `@keyframes fadeIn` |

### カウントアップの実装

```javascript
function animateCount(el, target, duration){
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(reduced || target===0){
    el.textContent = target;
    return;
  }
  const start = performance.now();
  const step = (now)=>{
    const t = Math.min((now-start)/duration, 1);
    const eased = 1 - (1-t)*(1-t); // easeOutQuad
    el.textContent = Math.round(eased*target);
    if(t<1) requestAnimationFrame(step);
    else el.textContent = target;
  };
  requestAnimationFrame(step);
}
```

- `matchMedia` で動的に `prefers-reduced-motion` をチェック
- モーション抑制時は瞬時に最終値を表示（カウントアップは行わない）
- `target===0` の場合もアニメーションをスキップ

---

## 11. 良い問題を作るためのガイド

### 問題文

- **1問1論点**: 複数の論点を同時に問うのは避ける。「Aかつ B」のような問題は分割する
- **明確な正解**: 「どちらかと言えば」のような曖昧な選択肢を避ける
- **引っかけに頼らない**: 本質的な理解を問う問題にする（単なる言い回しの違いで間違えさせない）

### 選択肢（multiple）

- **長さを揃える**: 正解だけ長かったり短かったりすると推測しやすい
- **すべて文法的に正しく**: 問題文と各選択肢をつないだとき自然な文になる
- **「上記すべて」「該当なし」は控えめに**: 使うと問題の意図が薄まる

### YES/NO

- **明確な主張文**: 「〜である」「〜できる」など事実を断定する形にする
- **二重否定を避ける**: 「〜ではないことはない」のような形は混乱を招く

### 並べ替え（sort）

- **各ステップが独立して意味を持つ**: 「AなしのBは成立しない」という強い依存は分かりやすくてよい（順序推論の手がかりになる）
- **3〜6項目に収める**: 多すぎると作業が面倒で理解を問う以前の問題になる
- **項目の長さをほぼ揃える**: 極端に長い項目があるとカードの高さがバラつき見づらい
- **明確な順序が存在するトピックを選ぶ**: 「一般的にはこの順」のような緩い順序は避ける

### 解説文

- **単に正解を繰り返さない**: 「なぜそれが正解か」を説明する
- **間違えやすいポイントに言及**: 他の選択肢がなぜ不適切かを1行で補足できると良い
- **2〜4文程度**: 長すぎる解説は読まれない

### 難易度のバランス

- **最初の1〜2問**: 基本確認。本文を読んでいれば解ける
- **中盤**: 応用・比較
- **終盤**: 総合的な理解を問う。細かい例外知識を問う「難問」を1つ入れてもよい

---

## 解説HTMLとのリンク

クイズHTMLと解説HTMLは相互にリンクさせる。

**クイズ側:**

```html
<!-- ヘッダー -->
<a class="back-link" href="解説HTMLファイル名.html">Back to notes</a>

<!-- 結果画面 -->
<a class="btn btn-ghost" href="解説HTMLファイル名.html">解説を見る</a>
```

**解説側（オプション）:**

解説HTMLの最後、Summary セクションの直後などに、クイズへの誘導リンクを追加してもよい。

```html
<p style="text-align:center;margin-top:2rem">
  <a class="btn btn-primary" href="タイトル_クイズ.html">理解度チェックに進む →</a>
</p>
```
