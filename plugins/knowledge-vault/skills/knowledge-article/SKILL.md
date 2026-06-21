---
name: knowledge-article
description: "技術ナレッジを、frontmatter（title / tags）＋「問題 → 原因 → 解決」の決まった型のファイルとして作成するスキル。後から tags で横断検索・再利用できるよう、記事フォーマットを揃えて1ファイル書き出す。出力は基本 Markdown（.md）、ユーザーが指定したときだけ HTML（.html）も可。「ナレッジ書いて」「知見をmd化」「これメモっといて」「ナレッジ記事作って」「HTMLで書いて」「knowledge article」などのキーワードでトリガー。"
---

# 技術ナレッジを定型フォーマットで1ファイルに書き出す

フォーマットを揃えるのは、後から tags で横断検索・再利用できる状態を保つため。1 記事 = 1 トピックの小さい粒度で、決まった型に当てはめて 1 ファイル書き出す。

## ワークフロー

1. 記録する「1 つの問題 or 知見」を 1 つに絞る。複数あれば記事を分ける（1 記事 = 1 トピック）。
2. フォーマットを [references/article-format.md](references/article-format.md) で確認する。
3. `title` と `tags`（技術名・トピック名を惜しまず複数）を決め、「何が起きたか → なぜか → どうしたか」で本文を書く。再現条件・環境・最小コードを残す。
4. 出力形式を決める。**基本は Markdown（`.md`）**。ユーザーが「HTML で」と明示したときだけ HTML（`.html`）で書き出す。
5. ファイルとして書き出す。ファイル名・保存先はユーザーの指示に従う。

## 出力形式

| 形式 | いつ使うか | テンプレート |
|---|---|---|
| **Markdown（既定）** | 指定が無いときは常にこちら | [references/article-format.md](references/article-format.md) |
| **HTML（オプション）** | ユーザーが「HTML で」と明示したときだけ | [references/article-format.html](references/article-format.html) |

- どちらの形式でも**中身のルール（1記事1トピック / tags 必須 / 日本語 / 最小コード）は同一**。構成（TL;DR → 問題 → 原因 → 解決 → まとめ）も揃える。
- HTML でも `tags` は `<meta name="keywords">` に必ず残す（横断検索の手がかりを失わないため）。

## 守ること

- 1 記事 = 1 トピック。迷ったら分割する。
- `tags` を省略しない（あとで検索する唯一の手がかり）。
- 日本語で書く。コードは最小再現に絞る。
- 整理しすぎて書くのをやめるより、粗くてもまず残す。

**テンプレート（`<…>` を差し替えて使う）**:
- Markdown（既定）: [references/article-format.md](references/article-format.md)
- HTML（オプション）: [references/article-format.html](references/article-format.html)
