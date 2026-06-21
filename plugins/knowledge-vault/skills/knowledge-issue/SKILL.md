---
name: knowledge-issue
description: "ナレッジ記事（Markdown）を gh コマンドで dev-knowledge リポジトリの GitHub Issue として登録するスキル。記事の frontmatter の title を issue タイトルに、tags を issue ラベルに、本文を issue 本文に反映する。「issueに登録」「issue化して」「ghでissue作って」「ナレッジをissueに」「register knowledge issue」などのキーワードでトリガー。記事そのものを作るのは knowledge-article。"
---

# Knowledge Issue

ナレッジ記事の Markdown を、`gh` コマンドで `dev-knowledge` リポジトリの GitHub Issue として登録する。記事を「後で docs に追加する」ための起票として使う。

---

## いつ使うか

- `knowledge-article` で書いた記事を、まず Issue として登録しておきたいとき
- すぐ docs にコミットせず、起票だけ先に済ませて後でまとめて記事化したいとき

## 前提条件

- `gh` (GitHub CLI) がインストール・認証済みであること（`gh auth status` で確認）。
- 対象リポジトリは **`dio0550/dev-knowledge`**。
- 登録元の記事 Markdown（frontmatter 付き）が手元にあること。無ければ先に `knowledge-article` で作る。

## 記事 → Issue のマッピング

| 記事の要素 | Issue の要素 |
|---|---|
| frontmatter `title` | Issue タイトル |
| frontmatter `tags` | Issue ラベル（`--label`） |
| frontmatter を除いた本文 | Issue 本文 |

## ワークフロー

### Step 1: 記事から要素を取り出す

- `title` … Issue タイトルにそのまま使う。
- `tags` … ラベル候補。
- 本文 … frontmatter（`---` で囲まれたブロック）を除いた部分。

### Step 2: ラベルの存在を確認・用意する

`gh` はラベルが存在しないとエラーになるため、無ければ作る。

```bash
# 既存ラベル一覧
gh label list --repo dio0550/dev-knowledge

# 足りないラベルを作成（例）
gh label create react --repo dio0550/dev-knowledge --color 1f6feb --force
```

- ラベルが多すぎて煩雑なら、代表的なタグ 1〜3 個に絞ってよい。残りは本文末尾に `tags: [...]` として残す。
- ラベル運用をしないなら Step 2 は省略し、`--label` を付けずに本文に tags を書く。

### Step 3: Issue を作成する

本文は一時ファイル経由で渡すのが安全（改行・記号崩れを防ぐ）。

```bash
# 本文を一時ファイルに用意（frontmatter を除いた本文 + tags メモ）
gh issue create \
  --repo dio0550/dev-knowledge \
  --title "<title>" \
  --label "<tag1>" --label "<tag2>" \
  --body-file /tmp/knowledge-issue-body.md
```

- frontmatter をそのまま本文に含めてもよい（記事化時にコピペしやすい）。その場合は本文先頭に frontmatter を残す。
- 作成後、`gh` が返す Issue URL をユーザーに伝える。

### Step 4: 報告

- 作成した Issue の URL とタイトル、付与したラベルを報告する。

## 注意点・例外

- **`gh` が使えない環境**（CI / リモート実行など）では `gh issue create` は失敗する。その場合は GitHub MCP ツール（`mcp__github__issue_write` 等）での起票にフォールバックするか、Issue 本文を提示してユーザーに手動登録を促す。
- ラベル未作成エラー（`could not add label`）が出たら Step 2 に戻ってラベルを作成する。
- タイトルは記事の `title` を尊重し、勝手に言い換えない。
- 1 記事 = 1 Issue。複数トピックをまとめて 1 Issue にしない。
