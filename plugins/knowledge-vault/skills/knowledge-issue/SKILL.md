---
name: knowledge-issue
description: "gh コマンドで dev-knowledge リポジトリ（dio0550/dev-knowledge）に GitHub Issue を作成するスキル。2つの使い方がある:(A) knowledge-article で作ったナレッジ記事を「記事化済みとして」issue に登録する、(B) 開発中に疑問に思った設計・気づき・調べたいことを、記事化せずそのまま issue として起票する。「issueに作って」「issue化」「ghでissue立てて」「これissueにしといて」「あとで調べたい」「設計の疑問をissueに」「register knowledge issue」などのキーワードでトリガー。"
---

# Knowledge Issue

`gh` コマンドで `dio0550/dev-knowledge` に GitHub Issue を作成するスキル。
「ナレッジとして残したいこと」を issue として起票する手順を提供する。

---

## 2つの使い方

| | 何を登録するか | 入力 |
|---|---|---|
| **A. 記事を登録** | `knowledge-article` で作った（or 既にある）ナレッジ記事 md | frontmatter 付きの `.md` |
| **B. 疑問を起票** | 開発中に疑問に思った設計・気づき・調べたいこと | 一言の課題・メモ |

どちらも登録先は `dio0550/dev-knowledge`。A は「まとまった知見の置き場」、B は「あとで記事化する種（TODO）」。

## 前提条件

- `gh` (GitHub CLI) がインストール・認証済みであること（`gh auth status` で確認）。
- 登録先は **`dio0550/dev-knowledge`**。

---

## A. ナレッジ記事を issue に登録する

`knowledge-article` で作った記事を、issue として登録する（docs に追加する前の起票、または記録として）。

### マッピング

| 記事の要素 | Issue の要素 |
|---|---|
| frontmatter `title` | Issue タイトル |
| frontmatter `tags` | Issue ラベル（`--label`） |
| 本文（frontmatter 込みでも可） | Issue 本文 |

### 手順

```bash
# 1) 足りないラベルがあれば作る（gh はラベルが無いとエラー）
gh label list --repo dio0550/dev-knowledge
gh label create react --repo dio0550/dev-knowledge --color 1f6feb --force

# 2) 本文は --body-file で渡す（改行・記号崩れを防ぐ）
gh issue create \
  --repo dio0550/dev-knowledge \
  --title "<記事の title>" \
  --label "<tag1>" --label "<tag2>" \
  --body-file <記事ファイル.md>
```

- frontmatter を本文に残しておくと、後で docs に移すときコピペしやすい。
- タイトルは記事の `title` を尊重し、勝手に言い換えない。

---

## B. 開発中の疑問・設計メモを issue に起票する

記事化するほどでもない／まだ調べきれていない「疑問・設計の迷い・あとで調べたいこと」を、その場で軽く issue にする。記事化の前段（種）として使う。

### 手順

```bash
# ラベルは付けても付けなくてもよい（例として question / design）
gh issue create \
  --repo dio0550/dev-knowledge \
  --title "<疑問を一言で>" \
  --label "question" \
  --body "$(cat <<'EOF'
## 疑問・背景
- 何に迷ったか / どういう状況で出てきた疑問か

## 調べたいこと / 仮説
- 確認したい点、現時点の仮説

## メモ
- 参考リンク、関連コードなど
EOF
)"
```

- 本文は軽くてよい。「背景・調べたいこと」の2点だけでも残す価値がある。
- 解決して知見がまとまったら、`knowledge-article` で記事化し、この issue を close する流れが基本。

---

## 注意点・例外

- **`gh` が使えない環境**（CI / リモート実行など）では `gh issue create` は失敗する。その場合は GitHub MCP ツール（`mcp__github__issue_write` 等）で起票するか、issue 本文を提示してユーザーに手動登録を促す。
- ラベル未作成エラー（`could not add label`）が出たらラベルを先に作成する。煩雑なら `--label` を省略してよい。
- 1 トピック = 1 Issue。複数の疑問・記事をまとめて 1 つにしない。
