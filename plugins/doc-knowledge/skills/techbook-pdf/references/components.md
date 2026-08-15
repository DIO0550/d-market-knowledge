# 部品リファレンス

そのままコピーして使えるHTML断片集。クラス名は `templates/book.css` と対応する。

## 目次

- [章と見出し](#章と見出し)
- [囲み（POINT / 注意 / 補足）](#囲みpoint--注意--補足)
- [側注](#側注)
- [用語定義](#用語定義)
- [例題](#例題)
- [章末演習と巻末解答](#章末演習と巻末解答)
- [コラム](#コラム)
- [コードブロック](#コードブロック)
- [図と表](#図と表)
- [章末まとめ](#章末まとめ)
- [索引と相互参照](#索引と相互参照)
- [文字の強調](#文字の強調)

---

## 章と見出し

```html
<section class="chapter">
  <header class="ch-opener">
    <p class="ch-num"></p>
    <h1>TLSと暗号化通信</h1>
    <div class="goals">
      <p class="goals-title">この章で学ぶこと</p>
      <ul>
        <li>TLSハンドシェイクの流れを追えるようになる</li>
        <li>証明書の検証が何を保証しているのかを説明できる</li>
      </ul>
    </div>
  </header>

  <h2>ハンドシェイクの流れ</h2>
  <h3>ClientHello</h3>
  <h4>拡張フィールド</h4>
</section>
```

- `.ch-num` は空要素のまま置く。`CHAPTER 02` が自動で入る。
- `h2` は `2.1`、`h3` は `2.1.1` が自動で付く。`h4` は番号なしの小見出し。
- 扉ページを立てたくない章は `<header class="ch-opener compact">`。

## 囲み（POINT / 注意 / 補足）

```html
<div class="callout point">
  <p class="co-title"></p>
  <p>HTTPはステートレスである。サーバはリクエスト間で状態を保持しない。</p>
</div>

<div class="callout warn">
  <p class="co-title">よくある間違い</p>
  <p>エラーを常に200で返し、ボディの中だけで失敗を示す設計は避ける。</p>
</div>

<div class="callout note">
  <p class="co-title">参考</p>
  <p>キャッシュ関連の仕様はRFC 9111に整理された。</p>
</div>
```

`point` は `.co-title` が空でも「POINT」の見出しが入る。タイトルを書けば「POINT　◯◯」になる。
`warn` は警告アイコン付き。`note` は淡いグレーの補足。

## 側注

```html
<p>HTTPは往復で成り立つプロトコルである<span class="snref">※1</span>。…</p>

<aside class="sidenote">
  <span class="sn-label">※1</span>
  正確にはHTTP/2以降は多重化されるが、意味論としての往復構造は変わらない。
</aside>
```

`aside` は**参照した段落の直後**に置く。外マージンに右寄せで流し込まれる。
`--no-sidenotes` でビルドした場合は外マージンに余地がないため、本文段の中に幅38%で
回り込む形に自動で切り替わる（紙面外にはみ出さない）。

## 用語定義

```html
<div class="termbox">
  <p class="term-name">冪等性（idempotency）</p>
  <p>同じリクエストを何回送ってもサーバの状態が1回送ったときと変わらない性質。</p>
</div>
```

## 例題

```html
<div class="example">
  <p class="ex-title">ステータスコードを選ぶ</p>
  <div class="ex-body">
    <p>メールアドレスが既に登録済みだった。返すべきステータスコードは何か。</p>
  </div>
  <div class="ex-answer">
    <p><strong>409 Conflict</strong>。リソースの現在の状態と矛盾するため。</p>
  </div>
</div>
```

`例題 1.2` の番号と「解答」の見出しは自動。`.ex-answer` を省けば問題だけの提示になる。

## 章末演習と巻末解答

```html
<section class="exercises">
  <h2>演習問題</h2>
  <ol>
    <li>GETが冪等でPOSTが冪等でない理由を説明せよ。</li>
    <li>301と302の違いを述べよ。</li>
  </ol>
</section>
```

`<h2>` には「第N章　」が前置される。`<ol>` の項目には `問1` `問2` のバッジが付く。
巻末解答は章の外に独立した節として置く。

```html
<section class="answers">
  <h1>演習問題の解答</h1>
  <div class="ans-item">
    <p class="ans-head">第1章　問1</p>
    <p>GETは取得のみでサーバ状態を変えないため…</p>
  </div>
</section>
```

## コラム

```html
<div class="column">
  <p class="col-title">CDNは誰のためのキャッシュか</p>
  <p>ブラウザキャッシュが「その人のため」なら、CDNキャッシュは「みんなのため」である。</p>
</div>
```

## コードブロック

```html
<figure class="code">
  <figcaption>最小のHTTPサーバ<span class="lang">python</span></figcaption>
  <pre><code class="language-python">def handle(request):
    return {"status": 200}</code></pre>
</figure>
```

- `class="language-xxx"` の言語名でPygmentsが着色する。省略すると推測になるので必ず書く。
- `<pre>` の直後に改行を入れない。1行目に空行が入る。
- キャプション不要なら `<figure>` を省いて `<pre><code>` だけでもよい。
- **1行の文字数上限**（a4:72 / b5:60 / a5:48）を守る。超えるとビルド時に警告が出る。

## 図と表

```html
<figure class="fig">
  <img src="diagram.svg" alt="ハンドシェイクの流れ">
  <figcaption>TLS 1.3のハンドシェイク</figcaption>
</figure>

<table>
  <caption>ステータスコードの分類</caption>
  <thead>
    <tr><th>範囲</th><th>分類</th><th class="wrap">代表例</th></tr>
  </thead>
  <tbody>
    <tr><td>2xx</td><td>成功</td><td>200 OK / 201 Created</td></tr>
  </tbody>
</table>
```

- `図 1.3` `表 1.1` の番号は自動。`<caption>` は `<table>` の**最初の子**に置く。
- `<th>` は既定で折り返さない。長い見出しには `class="wrap"` を付ける。
- SVGは `<img src>` でも直接埋め込みでもよい。画像パスは本文HTMLからの相対パス。

## 章末まとめ

```html
<div class="summary">
  <p class="sum-title">この章のまとめ</p>
  <ul>
    <li>HTTPはリクエストとレスポンスの往復で構成される</li>
  </ul>
</div>
```

## 索引と相互参照

```html
<p><span class="idx" data-term="公開鍵暗号" data-yomi="こうかいかぎあんごう">公開鍵暗号</span>で鍵を共有する。</p>

<h2 id="キャッシュ制御">キャッシュ制御</h2>
<p>詳しくは<a class="xref" href="#キャッシュ制御"></a>で扱う。</p>
```

- `.idx` は本文の見た目を変えない。同じ語を複数箇所でマークすると索引に複数ページが並ぶ。
- `data-term` を省くとタグの中身が索引語になる。`data-yomi` は五十音分類に使う。英字始まりの語は自動でアルファベット欄に入る。
- `.xref` のリンクテキストは空にする。`（→ p.12）` が自動で入る。

## 文字の強調

| 書き方 | 見え方 |
|---|---|
| `<strong>…</strong>` | 太字 |
| `<em>…</em>` | 主色の太字（斜体にはしない。和文で斜体は読みにくいため） |
| `<span class="marker">…</span>` | 蛍光ペン風のマーカー |
| `<span class="dot">…</span>` | 点線の傍線つき太字 |
| `<code>…</code>` | 本文中のインラインコード |
