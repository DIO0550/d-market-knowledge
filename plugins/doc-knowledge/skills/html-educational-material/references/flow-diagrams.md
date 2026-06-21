# フロー図パターン

技術的なプロセスフローを描画するためのパターン集。CSSグリッドで縦方向の整列を保証し、セマンティックな色分けでブロックの役割を表現する。

## 目次

1. [基本構造](#1-基本構造)
2. [グリッドの列構成](#2-グリッドの列構成)
3. [ブロックの種類と意味](#3-ブロックの種類と意味)
4. [エラー状態修飾子](#4-エラー状態修飾子)
5. [実装例：CBC暗号化フロー](#5-実装例cbc暗号化フロー)
6. [実装例：エラー伝播図](#6-実装例エラー伝播図)
7. [レジェンド（凡例）](#7-レジェンド凡例)
8. [設計原則](#8-設計原則)

---

## 1. 基本構造

```html
<figure>
  <div class="flow">
    <!-- 各行を .frow で構成 -->
    <div class="frow">
      <div class="rlabel">ラベル</div>
      <div class="block b-plain">P₁</div>
      <div class="arr">→</div>
      <div class="block b-plain">P₂</div>
      <div class="arr">→</div>
      <div class="block b-plain">P₃</div>
      <div class="arr">→</div>
      <div class="block b-plain">P₄</div>
    </div>
    <!-- 必要な行数だけ frow を繰り返す -->
  </div>
  <figcaption>
    <span class="fig-num">Fig. 1</span>フロー図の説明
  </figcaption>
</figure>
```

**構造の役割:**

- `<figure>`: フロー図全体のコンテナ。淡いグレー背景、罫線、`overflow-x: auto` で狭い画面ではスクロール
- `.flow`: 縦方向に `.frow` を並べるflexコンテナ。`min-width: 820px` でスクロール対応
- `.frow`: 1行を表すCSSグリッド（詳細は次節）
- `.rlabel`: 行の左端に付くラベル（「入力」「鍵」「出力」など）。JetBrains Monoで小さく
- `.block`: 処理や値を表すブロック。タイプに応じてクラスを付ける
- `.arr`: 矢印。`→`（右）、`↓`（下）、`↕`（双方向）などを使う
- `<figcaption>`: 図の説明。`.fig-num` で図番号を強調

---

## 2. グリッドの列構成

`.frow` のグリッドは **固定の8列構成** を使う。これにより全行の縦方向が自動的に整列する。

```css
.frow{
  display:grid;
  grid-template-columns:68px 110px 36px 110px 36px 110px 36px 110px;
  align-items:center;justify-items:center;gap:.3rem;
}
```

**列の意味:**

| 列 | 幅 | 用途 |
|----|-----|------|
| 1 | 68px | ラベル（`.rlabel`） |
| 2 | 110px | 1番目のブロック |
| 3 | 36px | 矢印 or XOR |
| 4 | 110px | 2番目のブロック |
| 5 | 36px | 矢印 or XOR |
| 6 | 110px | 3番目のブロック |
| 7 | 36px | 矢印 or XOR |
| 8 | 110px | 4番目のブロック |

**使わない列は空divで埋める:**

```html
<div class="frow">
  <div class="rlabel">IV</div>
  <div class="block b-iv">IV</div>
  <div></div><div></div><div></div><div></div><div></div><div></div>
</div>
```

## 3. ブロックの種類と意味

ブロックはセマンティックに色分けされている。**同じ役割には常に同じクラスを使う** と読み手が直感的に理解できる。

### 基本ブロック

```html
<div class="block b-plain">P₁</div>
<div class="block b-cipher">C₁</div>
<div class="block b-enc">E<sub>K</sub></div>
<div class="block b-dec">D<sub>K</sub></div>
<div class="block b-iv">IV</div>
```

| クラス | 役割 | 色 | 幅 |
|--------|------|-----|-----|
| `.b-plain` | 平文・入力 | 緑（`--ok`） | 104px |
| `.b-cipher` | 暗号文・出力 | オレンジ（`--warn`） | 104px |
| `.b-enc` | 暗号化処理 | 青（`--info`） | 104px |
| `.b-dec` | 復号処理 | 青（`--info`） | 104px |
| `.b-iv` | 初期値 | 紺（`--accent-ink`） | 84px（狭め） |

### XOR ブロック（丸形）

```html
<div class="block b-xor">⊕</div>
```

- 36x36pxの円形
- 36px幅の矢印列に収まるので、列の消費がなくレイアウトを崩さない
- 文字は `⊕` (U+2295)

### 補足付きブロック

ブロック内で値の意味を補足するとき:

```html
<div class="block b-plain">P₁<small>(0x48656C6C...)</small></div>
```

- `<small>` は小さい補足テキスト用（フォントサイズ0.66rem、透明度80%）
- ブロック内の2行目に表示される

---

## 4. エラー状態修飾子

復号エラーや破壊状態を示すための修飾子。ベースクラス（`.b-plain` など）に重ねて使う。

```html
<div class="block b-plain b-err">破壊された平文</div>
<div class="block b-plain b-partial">部分破壊</div>
<div class="block b-plain b-ok">正常復号</div>
```

| 修飾子 | 意味 | 色 |
|--------|------|-----|
| `.b-err` | 完全破壊・エラー | 赤（`--danger`） |
| `.b-partial` | 部分的影響 | オレンジ（`--warn`） |
| `.b-ok` | 正常（他がエラー状態のとき対比用） | 緑（`--ok`） |

これらは `!important` で元の色を上書きするので、**エラー伝播を示す図**で特に有用。例えばCBC復号で1バイト改ざん時、該当ブロックだけ `.b-err`、次ブロックは `.b-partial`、それ以降は `.b-ok` というパターン。

---

## 5. 実装例：CBC暗号化フロー

平文4ブロックをCBCモードで暗号化する流れ。

```html
<figure>
  <div class="flow">

    <!-- 平文行 -->
    <div class="frow">
      <div class="rlabel">平文</div>
      <div class="block b-plain">P₁</div>
      <div></div>
      <div class="block b-plain">P₂</div>
      <div></div>
      <div class="block b-plain">P₃</div>
      <div></div>
      <div class="block b-plain">P₄</div>
    </div>

    <!-- 矢印（下向き） -->
    <div class="frow">
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
    </div>

    <!-- XOR行（IV/前段暗号文とのXOR） -->
    <div class="frow">
      <div class="rlabel">IV</div>
      <div class="block b-xor">⊕</div>
      <div class="arr">→</div>
      <div class="block b-xor">⊕</div>
      <div class="arr">→</div>
      <div class="block b-xor">⊕</div>
      <div class="arr">→</div>
      <div class="block b-xor">⊕</div>
    </div>

    <!-- 矢印（下向き） -->
    <div class="frow">
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
    </div>

    <!-- 暗号化処理行 -->
    <div class="frow">
      <div class="rlabel">暗号化</div>
      <div class="block b-enc">E<sub>K</sub></div>
      <div></div>
      <div class="block b-enc">E<sub>K</sub></div>
      <div></div>
      <div class="block b-enc">E<sub>K</sub></div>
      <div></div>
      <div class="block b-enc">E<sub>K</sub></div>
    </div>

    <!-- 矢印（下向き） -->
    <div class="frow">
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
    </div>

    <!-- 暗号文行 -->
    <div class="frow">
      <div class="rlabel">暗号文</div>
      <div class="block b-cipher">C₁</div>
      <div></div>
      <div class="block b-cipher">C₂</div>
      <div></div>
      <div class="block b-cipher">C₃</div>
      <div></div>
      <div class="block b-cipher">C₄</div>
    </div>

  </div>
  <figcaption><span class="fig-num">Fig. 1</span>CBCモード暗号化：各ブロックは直前の暗号文（初回はIV）とXORしてから暗号化される</figcaption>
</figure>
```

**ポイント:**

- 縦方向の整列は8列グリッドで自動的に保たれる
- XORと暗号化の間のフィードバック線（C₁→⊕₂ など）は、本フローでは省略。詳細を示したい場合は SVG overlay か、XOR列に「IV/Cᵢ₋₁」の小さなラベル付きセルを追加する
- IVは先頭の `.rlabel` に置き、XOR行の左ラベルとして使う

---

## 6. 実装例：エラー伝播図

CBC復号で C₂ の1バイトが改ざんされた場合の影響範囲。

```html
<figure>
  <div class="flow">

    <div class="frow">
      <div class="rlabel">暗号文</div>
      <div class="block b-cipher b-ok">C₁</div>
      <div></div>
      <div class="block b-cipher b-err">C₂'<small>(改ざん)</small></div>
      <div></div>
      <div class="block b-cipher b-ok">C₃</div>
      <div></div>
      <div class="block b-cipher b-ok">C₄</div>
    </div>

    <div class="frow">
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
    </div>

    <div class="frow">
      <div class="rlabel">復号</div>
      <div class="block b-dec">D<sub>K</sub></div>
      <div></div>
      <div class="block b-dec">D<sub>K</sub></div>
      <div></div>
      <div class="block b-dec">D<sub>K</sub></div>
      <div></div>
      <div class="block b-dec">D<sub>K</sub></div>
    </div>

    <div class="frow">
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
      <div></div>
      <div class="arr">↓</div>
    </div>

    <div class="frow">
      <div class="rlabel">平文</div>
      <div class="block b-plain b-ok">P₁</div>
      <div></div>
      <div class="block b-plain b-err">P₂'<small>(完全破壊)</small></div>
      <div></div>
      <div class="block b-plain b-partial">P₃'<small>(1バイト反転)</small></div>
      <div></div>
      <div class="block b-plain b-ok">P₄</div>
    </div>

  </div>
  <figcaption><span class="fig-num">Fig. 2</span>1バイト改ざんの影響範囲：P₂は完全破壊、P₃は対応する1バイトのみ反転、P₁とP₄は無傷</figcaption>
</figure>
```

**ポイント:**

- `.b-ok` / `.b-err` / `.b-partial` で影響範囲を色分け
- `<small>` で破壊の性質を短く注記
- 凡例（`.legend`）を続けて配置すると理解が深まる

---

## 7. レジェンド（凡例）

```html
<div class="legend">
  <div class="legend-item">
    <div class="legend-color" style="background:var(--ok-soft);border-color:var(--ok)"></div>
    <span>平文</span>
  </div>
  <div class="legend-item">
    <div class="legend-color" style="background:var(--warn-soft);border-color:var(--warn)"></div>
    <span>暗号文</span>
  </div>
  <div class="legend-item">
    <div class="legend-color" style="background:var(--info-soft);border-color:var(--info)"></div>
    <span>暗号化/復号処理</span>
  </div>
  <div class="legend-item">
    <div class="legend-color" style="background:var(--danger-soft);border-color:var(--danger)"></div>
    <span>破壊・エラー</span>
  </div>
</div>
```

- `.legend-color` は16x16pxの色見本（インラインstyleで色を指定）
- フロー図の直下、または `<figure>` の外側に配置
- 同じ色を使う複数の図がある場合は、最初の図の下に一度だけ表示すれば十分

---

## 8. 設計原則

### 1. 縦方向の整列を最優先

フロー図の読みやすさは、**縦に並んだブロックが正確に揃っていること** で決まる。CSSグリッドを使うことで、要素の有無に関わらず列位置が固定される。

### 2. 色の一貫性

同じ役割のブロックは、ドキュメント全体で同じクラス（＝同じ色）を使う。「平文はいつも緑、暗号文はいつもオレンジ、処理はいつも青」という期待を裏切らない。

### 3. ラベルは左端に統一

行の意味（平文行、暗号文行、鍵行など）は `.rlabel` として左端に配置する。右端や中央に分散させると、読み手の視線が迷う。

### 4. スクロール可能を前提に設計

`.flow` の `min-width: 820px` により、狭い画面では横スクロールになる。ブロック数を減らして収めるのではなく、**本来の情報量を保ったまま横スクロールさせる** 方針（参照: memoryの「full detail over simplified」原則）。

### 5. 小さな画面では自動調整

`@media(max-width:640px)` で `.frow` の列幅が自動で狭くなる（86px / 28px）。そのため、極端に長いラベルや説明文は `.block` に入れない。必要なら `<small>` を使う。

### 6. 矢印は方向を明示

- 右向き: `→` (U+2192)
- 下向き: `↓` (U+2193)
- 上向き: `↑` (U+2191)
- 双方向: `↕` (U+2195) または `⇄` (U+21C4)

通常のフローは上→下、左→右に流れる。逆向きの矢印は例外的に使い、読み手を混乱させないよう凡例で補足する。

---

## よくある失敗パターン

| 失敗 | 原因 | 対策 |
|------|------|------|
| ブロックが縦にズレる | 空の `<div>` で列を埋めていない | 使わない列も `<div></div>` を置く |
| 行ごとに列数が違う | 一部の行で列数が8未満 | すべての `.frow` で厳密に8要素を保つ |
| モバイルで崩れる | ブロック内のテキストが長すぎる | `<small>` を使うか、メインテキストを短縮 |
| 色の意味が伝わらない | レジェンド未掲載 | 最初の図の直下に `.legend` を必ず配置 |
