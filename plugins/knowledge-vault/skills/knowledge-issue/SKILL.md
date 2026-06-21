---
name: knowledge-issue
description: "gh コマンドで dev-knowledge リポジトリ（dio0550/dev-knowledge）に GitHub Issue を作成するスキル。登録するナレッジには「どうリポジトリに反映するか」を表す2種類のラベルを必ず1つ付ける: knowledge:pr（ブランチで調査しPRでナレッジmdを作る）/ knowledge:direct（mainで作業しmd化して直接push）。使い方は(A) knowledge-article で作った記事を登録、(B) 開発中の疑問・設計メモを起票、の2通り。「issueに作って」「issue化」「ghでissue立てて」「これissueにしといて」「あとで調べたい」「設計の疑問をissueに」「register knowledge issue」などのキーワードでトリガー。"
---

# ナレッジを dev-knowledge の issue として起票する

「まとまった記事」も「開発中にふと湧いた疑問」も、`gh` で `dio0550/dev-knowledge` の issue に落とし込む。記事化の前後どちらの段階でも知見を取りこぼさないための受け口。

---

## 進め方ラベル（2種類・必須）

issue には「そのナレッジ md を**どうリポジトリに反映するか**」を表すラベルを **必ず 1 つ**付ける。後で対応するときの進め方が一目で分かるようにするため。

| ラベル | 進め方 | 向くケース |
|---|---|---|
| `knowledge:pr` | ブランチを切ってリポジトリ側で調査し、ナレッジ md を作成して **PR を出す**（レビュー経由で main へ） | 裏取り・調査が要る、レビューしたい、複数ファイルに渡る |
| `knowledge:direct` | **main で作業**して内容を md 化し、**直接 push** する | すでに結論が出ている軽い知見、自分用メモ、即反映したい |

迷ったら `knowledge:pr`。後から直 push に切り替えるのは簡単だが、逆（push 済みを PR に戻す）は手戻りになるため。

### ラベルの用意（初回のみ）

ラベルが無いと `gh` はエラーになる。無ければ作る。

```bash
gh label create "knowledge:pr"     --repo dio0550/dev-knowledge --color 1f6feb --description "調査してPRでナレッジmdを作る" --force
gh label create "knowledge:direct" --repo dio0550/dev-knowledge --color 0e8a16 --description "mainで作業してmd化し直接pushする" --force
```

---

## 2つの使い方

| | 何を登録するか | 入力 |
|---|---|---|
| **A. 記事を登録** | `knowledge-article` で作った（or 既にある）ナレッジ記事 md | frontmatter 付きの `.md` |
| **B. 疑問を起票** | 開発中に疑問に思った設計・気づき・調べたいこと | 一言の課題・メモ |

どちらも登録先は `dio0550/dev-knowledge`。A は「まとまった知見の置き場」、B は「あとで記事化する種（TODO）」。**いずれも進め方ラベルを 1 つ付ける**。

## 前提条件

- `gh` (GitHub CLI) がインストール・認証済みであること（`gh auth status` で確認）。
- 登録先は **`dio0550/dev-knowledge`**。
- 進め方ラベル（`knowledge:pr` / `knowledge:direct`）が用意済みであること（上記「ラベルの用意」参照）。

---

## A. ナレッジ記事を issue に登録する

`knowledge-article` で作った記事を issue として登録する。

- タイトル: 記事 frontmatter の `title`（勝手に言い換えない）
- 本文: 記事本文（frontmatter 込みでも可。後で docs に移すときコピペしやすい）
- ラベル: 進め方ラベルを 1 つ

```bash
gh issue create \
  --repo dio0550/dev-knowledge \
  --title "<記事の title>" \
  --label "knowledge:pr" \
  --body-file <記事ファイル.md>
```

---

## B. 開発中の疑問・設計メモを issue に起票する

記事化するほどでもない／まだ調べきれていない「疑問・設計の迷い・あとで調べたいこと」をその場で軽く issue にする。調査が要ることが多いので **`knowledge:pr` が基本**。

```bash
gh issue create \
  --repo dio0550/dev-knowledge \
  --title "<疑問を一言で>" \
  --label "knowledge:pr" \
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

- 解決して知見がまとまったら、`knowledge-article` で記事化し、この issue を close する流れが基本。

---

## 注意点・例外

- 進め方ラベルは A/B どちらでも **必ず 1 つ**付ける。両方付けない／両方付けるはしない。
- **`gh` が使えない環境**（CI / リモート実行など）では `gh issue create` は失敗する。その場合は GitHub MCP ツール（`mcp__github__issue_write` 等）で起票するか、issue 本文を提示してユーザーに手動登録を促す。
- ラベル未作成エラー（`could not add label`）が出たら「ラベルの用意」を先に実行する。
- 1 トピック = 1 Issue。複数の疑問・記事をまとめて 1 つにしない。
