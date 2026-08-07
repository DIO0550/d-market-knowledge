---
name: knowledge-lookup
description: "dev-knowledge（dio0550/dev-knowledge）に蓄積済みのナレッジを、公開サイトの JSON API から取得して調べるスキル。/api/docs.json で全記事の目次を 1 回取り、関係する記事の本文（Markdown）だけを contentUrl で取得する。タグから絞りたいときは /api/tags.json を使う。ベクタ検索・埋め込み・リポジトリの clone は不要で、公開 URL への HTTPS 取得だけで完結する。「前に調べたやつある？」「dev-knowledgeに書いてある？」「既存ナレッジ調べて」「過去の知見から探して」「このエラー前もハマった気がする」「ナレッジベース検索」「search dev-knowledge」などのキーワードでトリガー。書く側（knowledge-article / knowledge-issue / knowledge-harvest）に対する読み取り側の入口。"
---

# dev-knowledge に貯めたナレッジを JSON API から引く

`knowledge-article`（書く）/ `knowledge-issue`（起票する）/ `knowledge-harvest`（会話から集める）が**書き込み側**なのに対し、このスキルは**読み取り側**。すでに貯めた知見を引き当てて、同じ調査を二度やらないための入口。

dev-knowledge の公開サイトはビルド時に AI 向けの JSON を出力している。**記事ページの HTML をスクレイピングしない。JSON API を使う。**

ベースは `https://DIO0550.github.io/dev-knowledge`。

## エンドポイント

| エンドポイント | 内容 |
|---|---|
| `/api/docs.json` | **全記事の目次**。各記事の `title` / `url` / `category` / `tags` と、本文を返す `contentUrl` |
| `/api/docs/<id>.json` | 記事の本文（frontmatter を除いた Markdown）。`contentUrl` が指す先 |
| `/api/tags.json` | 全タグ。各タグの `name` / `count` と、タグ別 JSON の `url` |
| `/api/tags/<tag>.json` | そのタグが付いた記事の一覧（`docs.json` と同じ形） |
| `/api/index.json` | 上記の URL をまとめたエントリポイント |

目次は全体で 60KB 程度（記事数 100 未満）なので、**丸ごと読んでよい**。チャンク分割も埋め込みも要らない。

---

## ワークフロー

進捗チェックリストをコピーして進める：

```
- [ ] Step 1: /api/docs.json を取得して目次を読む
- [ ] Step 2: title / tags / category から候補を絞る
- [ ] Step 3: 候補の contentUrl で本文を取得する
- [ ] Step 4: 出典（記事 URL）付きで答える
```

### Step 1: 目次を取得する

```bash
curl -s https://DIO0550.github.io/dev-knowledge/api/docs.json
```

`WebFetch` 等のツールでも可。**1 回の取得で全記事のタイトル・カテゴリ・タグが揃う**ので、まずこれを読む。

### Step 2: 候補を絞る

目次の `title` / `tags` / `category` を見て、関係しそうな記事を選ぶ。タイトルは「〜は〜ではなく〜で解く」のように結論が入っている粒度なので、タイトルとタグだけでかなり判別できる。

**タグが先に決まっているとき**（「react の hooks 周りで」など）は目次の代わりに `/api/tags.json` を取り、該当タグの `url` を辿る。返る形は `docs.json` と同じで `contentUrl` も入っているため、目次を経由せず本文へ行ける。

絞り込みは 1 件に決め打ちしない。**関連しそうなものは複数取る**（横断はタグで担保する設計なので、隣接する記事に答えがあることが多い）。

### Step 3: 本文を取得する

候補の `contentUrl` を取得する。返る `content` は frontmatter を除いた Markdown 本文なので、そのまま読める。

```bash
curl -s "<docs.json の contentUrl をそのまま>"
```

### Step 4: 出典付きで答える

答えには**記事の `url`（公開サイトの記事ページ）を必ず添える**。どのナレッジに基づく回答かを追えるようにするため。複数記事を使ったら全部挙げる。

---

## 守ること

- **URL を文字列として組み立てない。** レスポンスに入っている `url` / `contentUrl` をそのまま辿る。タグ名と slug は一致しないことがあり（`AbortController` → `abort-controller`）、日本語は percent-encode される。
- **記事ページの HTML をパースしない。** 本文が要るなら `contentUrl`。
- **無いものを「ありそう」で埋めない。** 目次に該当が無ければ「dev-knowledge には無い」と明言する。そのうえで下記の導線に繋ぐ。
- 取得した本文の内容と、その場で推測したことを混ぜない。どこまでが記事の記述かを分けて書く。

## 見つからなかったとき

ナレッジが無いのは**起票のチャンス**。調べ直した結果が出たら、`knowledge-article` で記事にする / `knowledge-issue` で issue に落とす、へ繋ぐ。「無かった」で終わらせない。

## 関連スキル

| スキル | 役割 | このスキルとの関係 |
|---|---|---|
| `knowledge-article` | 知見を frontmatter 付き md 記事にする | 引いて無かった知見を、調べ直して記事化する先 |
| `knowledge-issue` | 1 件を dev-knowledge の issue に起票 | 引いて無かった疑問を「あとで調べる」として残す先 |
| `knowledge-harvest` | 会話からナレッジ候補を洗い出して起票 | 逆向き（会話 → リポジトリ）。こちらはリポジトリ → 回答 |

## 前提条件

- 公開サイト（`https://DIO0550.github.io/dev-knowledge`）へ HTTPS で到達できること。**パブリックサイトなので `gh` の認証もリポジトリの clone も要らない。**
- エンドポイントが 404 のときは、そのサイトに JSON API がまだデプロイされていない。リポジトリの `dev-knowledge/docs/` 配下の `.md` を直接読む（`gh search code --repo dio0550/dev-knowledge` や raw URL）にフォールバックし、JSON API が無い旨をユーザーに伝える。
