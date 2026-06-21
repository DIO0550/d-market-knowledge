# ナレッジ記事フォーマット（HTML 版・オプション）

通常は [article-format.md](article-format.md) の **Markdown が基本**。ユーザーが明示的に「HTML で」と指定したときだけこの型を使う。

Markdown 版と**同じ構成（TL;DR → 問題 → 原因 → 解決 → まとめ）**を HTML に落とし込む。frontmatter の `title` / `tags` は、横断検索の手がかりを失わないよう `<meta>` に埋め込む。

## Contents

- メタ情報の持たせ方
- 完成テンプレート
- 守るルール

---

## メタ情報の持たせ方

Markdown の frontmatter に相当する情報を `<head>` に入れる。

- `title`: `<title>` と `<h1>` の両方に同じ文言を入れる。
- `tags`: `<meta name="keywords">` にカンマ区切りで入れる（検索の起点なので惜しまない）。`<meta name="article:tag">` を tag ごとに並べてもよい。

## 完成テンプレート

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title><!-- 簡潔なタイトル --></title>
  <meta name="keywords" content="<!-- tech, topic, ... -->">
  <meta name="description" content="<!-- 一行サマリ（任意） -->">
</head>
<body>
  <article>
    <h1><!-- 簡潔なタイトル --></h1>

    <section>
      <h2>TL;DR</h2>
      <ul>
        <li>結論を箇条書きで先に。</li>
      </ul>
    </section>

    <section>
      <h2>遭遇した問題</h2>
      <ul>
        <li>何が起きたか。再現条件・環境（バージョン等）を残す。</li>
      </ul>
    </section>

    <section>
      <h2>原因</h2>
      <ul>
        <li>なぜそうなるか。</li>
      </ul>
    </section>

    <section>
      <h2>解決</h2>
      <ul>
        <li>どう直したか / どう設計したか。</li>
      </ul>
      <pre><code class="language-ts">
// 最小再現に絞ったコード。動かない例と動く例を併記すると後で役立つ。
      </code></pre>
    </section>

    <section>
      <h2>まとめ / 参考</h2>
      <ul>
        <li>参考リンクや一行まとめ。</li>
      </ul>
    </section>
  </article>
</body>
</html>
```

- 問題ではなく設計指針などの知見系は、`<h2>遭遇した問題</h2>` を「このドキュメントの射程」等に置き換えてよい（Markdown 版と同じ）。
- コード内の `<` `>` `&` は実体参照（`&lt;` `&gt;` `&amp;`）でエスケープする。

## 守るルール

- 出力形式が変わるだけで、**中身のルールは Markdown 版と同一**（1 記事 = 1 トピック / tags 省略しない / 日本語 / 最小コード）。
- `tags` は必ず `<meta name="keywords">` に残す。HTML だからといって省略しない。
- ファイル拡張子は `.html`。保存先はユーザーの指示に従う。
