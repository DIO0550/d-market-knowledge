---
name: techbook-pdf
description: 技術参考書・教科書スタイルのPDFを生成するスキル。HTMLと印刷用CSS（WeasyPrint）で、表紙・章扉・ページ番号つき自動目次・柱（ランニングヘッド）・ノンブル・側注・POINT囲み・例題・章末演習問題・コラム・図表番号・自動索引を備えた日本語組版のPDFを組む。A4/B5/A5の判型プリセットに対応。「参考書っぽいPDF」「技術書風のPDF」「教科書みたいなPDF」「HTMLからPDF」「書籍レイアウト」「章立てのPDF資料」「索引付きPDF」「印刷用の解説書」「テキスト教材のPDF」などのキーワードでトリガー。通読させる解説資料をPDFで作る場面では積極的に使用すること。画面で読ませるHTML教材は html-educational-material が担当する。
---

# techbook-pdf

本文をHTML断片で書き、`build_pdf.py` に渡すと参考書レイアウトのPDFになる。
目次・索引・図表番号・ページ相互参照は**すべて自動生成**なので、手で番号を振らない。

## ワークフロー

1. **判型と構成を決める** — 未指定なら `b5`（技術書の標準判型）。章立てをユーザーと合意する。
2. **本文HTML断片を書く** — `<section class="chapter">` の並びだけを書く。`<html>` や `<head>` は書かない。骨格は [templates/content-skeleton.html](templates/content-skeleton.html)、各部品の書式は [references/components.md](references/components.md)。
   概念の説明には**図を積極的に入れる**。インラインSVGのパターン集（構成図・シーケンス図・レイヤ図・
   フロー図・攻撃フロー図、および人物／攻撃者／サーバ等のアイコン集）は
   [references/diagrams.md](references/diagrams.md)。
3. **ビルドする** — 下記コマンド。警告が出たら潰す。
4. **必ず目視確認する** — `pdftoppm -png -r 80 book.pdf pg` で画像化し、最低でも表紙・目次・本文・索引の4枚を `view` で見る。組版は見ないと崩れに気づけない。
5. **成果物を渡す** — PDFを作業ディレクトリに出力し、ファイルパスをユーザーに伝える。

## ビルド

```bash
python3 scripts/build_pdf.py content.html -o book.pdf \
  --preset b5 \
  --title "実践Webプロトコル入門" \
  --subtitle "HTTPからTLSまで、手を動かして理解する" \
  --kicker "TECH REFERENCE"
```

| オプション | 既定 | 用途 |
|---|---|---|
| `--preset` | `b5` | `a4` / `b5` / `a5` |
| `--accent` | `#1b4f8a` | 主色。`--accent-weak` は淡色（囲み背景）を必ず対で指定する |
| `--toc-depth` | `2` | 目次に載せる見出しの深さ（1〜3） |
| `--author` / `--meta` | — | 表紙の著者名 / 刊記（版数・年）。**任意**。どちらも無ければ表紙下部ごと省かれる |
| `--kicker` | — | 表紙上部の小見出し（`TECH REFERENCE` など） |
| `--no-cover` / `--no-toc` / `--no-index` | — | 各パートを省く |
| `--no-sidenotes` | — | 側注を使わない。外マージンが狭い左右対称の版面になる |
| `--keep-html` | — | 中間HTMLを残す。崩れの原因調査に使う |
| `--install-deps` | — | 不足依存をロックから `.venv` に導入する（下記） |

## 依存とその導入

WeasyPrint / BeautifulSoup / Pygments に依存するが、**スクリプトは依存を勝手に入れない**。
不足していればコマンドを示して停止するので、初回だけ次を実行する。

```bash
python3 scripts/build_pdf.py --install-deps content.html -o book.pdf --preset b5 --title "…"
```

`scripts/requirements.lock.txt` に全17パッケージのバージョンと sha256 が固定してあり、
これを `--require-hashes` 付きで `scripts/.venv` に導入する。導入先はこの venv だけで、
システムの Python には書き込まない。2回目以降は自動で venv 側に切り替わるので指定不要。

ハッシュ不一致で失敗したら**取り込まずに止める**。配布物がすり替わった可能性がある。

### ロックは固定して使う（定期更新しない）

このロックは検証済みで、**そのまま使い続けるのが既定**。追従する理由が無いのに版を上げると、
そのたびに未検証のコードを取り込むことになり、かえって危険が増える。

`update_lock.py --check` は「上流に新しい版が出ているか」を見るだけで、**健全性チェックでは
ない。古い＝問題ではないので、これが「古い」と言っても更新しなくてよい。**

更新するのは理由があるときだけ。

- 依存に脆弱性・悪性パッケージの報告が出た
- 必要な修正や機能が新しい版に入っている
- 新しい Python でビルドが通らなくなった

### 更新する場合の手順

`python3 scripts/update_lock.py` で作り直し、**バージョンとハッシュの差分を必ずレビューして**
からコミットする。`update_lock.py` は**最新版を選ばない**。公開から14日を過ぎた版のうち
最も新しいものを採る（`--min-age` で変更可）。リリースが乗っ取られた場合、発覚するのは
公開から数日後になるため、最新版を追うとその窓に自分から入ることになる。

あわせて次も確認する。ロック済みバージョンの安全性は、ハッシュ固定では保証されない。

```bash
# マルウェア判定（Aikido Intel。pip も対象）
npm install -g @aikidosec/safe-chain && safe-chain setup-ci
pip install -r scripts/requirements.lock.txt --require-hashes --only-binary :all: --no-deps

# 既知の脆弱性・悪性パッケージ報告（OSV は MAL- として悪性パッケージも収録している）
curl -s -X POST https://api.osv.dev/v1/querybatch -d '{"queries":[…]}'
```

長く更新の無かったパッケージが突然リリースされていたら、取り込む前に**配布物と
公開ソースを突き合わせる**。乗っ取りならタグに無いコードが配布物に入る。

```bash
pip download --no-deps --no-binary :all: <pkg>==<ver> -d /tmp/x   # 実行はしない
git clone <repo> && git checkout v<ver>
diff -r <repo>/<pkg> /tmp/x/<pkg>-<ver>/<pkg>
```

**`webencodings` 0.6.x はこの手順で確認済み（乗っ取りではない）。** 2017年の 0.5.1 以降
休眠していたが、2026-08-15 に 0.6.0 と 0.6.1 が同日公開された。調べた結果、
WeasyPrint 一式を維持する CourtBouillon への移管で、配布物は `CourtBouillon/webencodings`
のタグ `v0.6.1` と完全一致した（同日2連続なのは 0.6.0 のPyPIリンクが旧所在のままだったため）。
旧所在 `gsnedders/python-webencodings` は2017年で止まっているので、そちらを見ると
「GitHubが更新されていない」ように見える。現所在は `CourtBouillon/webencodings`。

なお現在 0.5.1 に留めているのは上記14日ルールの結果であって、0.6.1 を危険と判断した
からではない。次回ロック更新時には期間を満たして自然に上がる。

## 本文HTMLの骨格

```html
<section class="chapter">
  <header class="ch-opener">          <!-- 章扉（独立1ページ） -->
    <p class="ch-num"></p>            <!-- 中身は空。CHAPTER 01 は自動 -->
    <h1>HTTPとその周辺</h1>
    <div class="goals">
      <p class="goals-title">この章で学ぶこと</p>
      <ul><li>…</li></ul>
    </div>
  </header>

  <h2>HTTPの基本構造</h2>            <!-- 1.1 は自動採番 -->
  <p>本文。</p>
  <h3>リクエストの実際</h3>          <!-- 1.1.1 は自動採番 -->

  <section class="exercises">        <!-- 章末演習 -->
    <h2>演習問題</h2>
    <ol><li>…</li></ol>
  </section>
</section>
```

章は必ず奇数（右）ページ起こしになる。`.ch-opener` に `compact` を足すと扉ページを立てず本文に続ける。

## 部品の早見表

詳しい書式と実例は [references/components.md](references/components.md) を読む。

| クラス | 用途 |
|---|---|
| `.callout.point` / `.warn` / `.note` | POINT囲み / 注意 / 補足 |
| `.sidenote` + `.snref` | 側注と本文中の参照マーク |
| `.termbox` | 用語定義 |
| `.example` | 例題（問題＋解答が一体） |
| `.exercises` / `.answers` | 章末演習問題 / 巻末解答 |
| `.column` | コラム |
| `figure.code` | ファイル名つきコードブロック |
| `figure.fig` / `<table><caption>` | 図 / 表（番号は自動）。図の描き方は [references/diagrams.md](references/diagrams.md) |
| `.summary` | 章末まとめ |
| `.idx` | 索引語のマーキング |
| `.xref` | ページ相互参照（`（→ p.12）`が自動で入る） |
| `.marker` / `.dot` | 蛍光ペン風 / 点線傍線の強調 |

## 電子書籍リーダーでの利用

PDFのしおり（アウトライン）が章・節・項の3階層で自動生成されるので、Kindleなどの
サイドバー目次からページジャンプできる。表示は「第1章　HTTPとその周辺」「1.1　HTTPの基本構造」と
本文の目次と同じ番号表記になる。目次・索引・相互参照の各リンクもクリック可能。

しおりが出ない・階層がおかしいときは、見出しに `.ch-opener h1` / `h2` / `h3` 以外のタグを
使っていないか確認する。`h4` は意図的にしおりから外してある。

## 守るべき制約

**コードの1行は判型の上限文字数（a4:72 / b5:60 / a5:48）に収める。** 超えると自動折り返しになり、続き行が新しい行に見えて可読性が落ちる。ビルド時に警告が出るので、変数名の短縮や改行の挿入で必ず解消する。

**索引語には読みを付ける。** `<span class="idx" data-term="公開鍵暗号" data-yomi="こうかいかぎあんごう">公開鍵暗号</span>` のように `data-yomi` を書く。無いと漢字の先頭文字で分類され「その他」に落ちる。

**番号を手で書かない。** 章番号・節番号・図表番号・例題番号・ページ番号・目次・索引はすべてCSSカウンタとスクリプトが解決する。本文に「図1.3」と直書きすると、あとで章を入れ替えたときに壊れる。

**IDは自動付与される。** 相互参照したい見出しだけ明示的に `id` を付け、`<a class="xref" href="#その-id"></a>` で参照する。リンクテキストは空でよい（`（→ p.N）` が自動で入る）。

**図中の文字は版面幅で圧縮される。** `viewBox` 幅420が版面いっぱいに縮むため、
`font-size: 9px` はb5で7.2pt、a5では5.9ptにしかならない。主ラベルは11px、補助は9pxを下限にする。

**攻撃者は赤系で塗り分ける。** セキュリティの図では正規の登場人物を主色、攻撃者を `#b3541e` にし、
攻撃者の活動範囲を破線で囲む。攻撃図を出したら対になる対策図も続けて置く。

**図のスタイルはSVGの中に書く。** WeasyPrintは `book.css` をインラインSVGに適用しない。
外側のクラスや `currentColor` に頼ると矩形が黒く塗り潰される。詳細は
[references/diagrams.md](references/diagrams.md)。

**著者名を勝手に作らない。** `--author` は任意で、ユーザーが名前を挙げていないなら指定しない。
未指定なら表紙は書名・副題だけの構成に自動で組み直される。刊記（`--meta`）も同様。

**`<p>` の字下げは自動。** 和文の作法として本文段落は1字下げされる。囲みの中や箇条書きは自動で字下げなしになるので、`<br>` や全角スペースで調整しない。

## つまずいたら

WeasyPrint固有の制約（`counter-reset: page` が `target-counter` を壊す、圏点が使えない、コードのインデントが消える等）と対処は [references/troubleshooting.md](references/troubleshooting.md) にまとめてある。レイアウトが想定と違うときは先にここを見る。
