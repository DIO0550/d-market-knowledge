---
name: knowledge-article
description: "技術ナレッジを dev-knowledge リポジトリの記事フォーマットに沿った Markdown ファイルとして作成するだけのスキル。frontmatter（title / tags）＋「問題 → 原因 → 解決」の決まった型で1ファイル書き出す。issue 登録はしない（それは knowledge-issue）。「ナレッジ書いて」「知見をmd化」「これメモっといて」「ナレッジ記事作って」「knowledge article」などのキーワードでトリガー。"
---

# 技術ナレッジを定型フォーマットで1ファイルに書き出す

フォーマットを揃えるのは、後から tags で横断検索・再利用できる状態を保つため。書き出すところまでが責務で、起票（`knowledge-issue`）や公開とは切り離す。

## スコープ

- やる: ナレッジを所定フォーマットの `.md` ファイルとして 1 本作る。
- やらない: GitHub Issue 登録（→ `knowledge-issue`）、コミット / PR、デプロイ。

## ワークフロー

1. 記録する「1 つの問題 or 知見」を 1 つに絞る。複数あれば記事を分ける（1 記事 = 1 トピック）。
2. フォーマットを [references/article-format.md](references/article-format.md) で確認する。
3. `title` と `tags`（技術名・トピック名を惜しまず複数）を決め、「何が起きたか → なぜか → どうしたか」で本文を書く。再現条件・環境・最小コードを残す。
4. `.md` ファイルとして書き出す。保存先は references の「保存先」に従う。

## 守ること

- 1 記事 = 1 トピック。迷ったら分割する。
- `tags` を省略しない（あとで検索する唯一の手がかり）。
- 日本語で書く。コードは最小再現に絞る。
- 整理しすぎて書くのをやめるより、粗くてもまず残す。

**フォーマット詳細（frontmatter・本文テンプレート・保存先）**: [references/article-format.md](references/article-format.md)
