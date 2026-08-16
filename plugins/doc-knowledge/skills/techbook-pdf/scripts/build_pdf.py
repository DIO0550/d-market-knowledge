#!/usr/bin/env python3
"""
techbook-pdf : 本文HTML断片 → 参考書スタイルのPDF

やること:
  1. 見出しへのID自動付与
  2. 目次の自動生成（ページ番号はCSSのtarget-counterが解決）
  3. 索引の自動生成（<span class="idx" data-term="..." data-yomi="...">）
  4. コードのシンタックスハイライト（Pygments）
  5. 判型プリセットの@page注入 → WeasyPrintでPDF出力

使い方:
  python3 build_pdf.py content.html -o book.pdf --preset b5 \
      --title "実践TCP/IP入門" --subtitle "..." --author "著者名"

  --keep-html を付けると中間HTMLを残す（レイアウト調査用）。
"""

import argparse
import html
import importlib
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------- 依存の確保
#
# 依存を黙って pip install しない。サプライチェーン対策として:
#   1. requirements.lock.txt でバージョンと sha256 を固定する（後から出た
#      改竄リリースを自動で拾わない。検証は pip の --require-hashes が行う）
#   2. 導入は --install-deps を明示したときだけ行う（import の副作用にしない）
#   3. 入れる先はこのスキル専用の .venv に限る（システムの Python を汚さない）
#   4. wheel のみ許可し、索引は pypi.org に固定する（sdist のビルド時コード実行と、
#      環境変数や pip.conf による索引すり替えを封じる）
# 既に依存が入っている環境では、この節は何もせず素通りする。

SKILL_DIR = Path(__file__).resolve().parent
LOCK = SKILL_DIR / "requirements.lock.txt"
VENV = SKILL_DIR / ".venv"

# import 名 → パッケージ名
REQUIRED = {"bs4": "beautifulsoup4", "weasyprint": "weasyprint", "pygments": "pygments"}

_REEXEC_GUARD = "TECHBOOK_PDF_IN_VENV"


def _missing() -> list[str]:
    """未導入のパッケージ名を返す。"""
    importlib.invalidate_caches()
    out = []
    for mod, pkg in REQUIRED.items():
        try:
            importlib.import_module(mod)
        except ImportError:
            out.append(pkg)
    return out


def _venv_python() -> Path | None:
    exe = VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return exe if exe.exists() else None


def _install_deps() -> None:
    """ロックから .venv に導入する。ハッシュが合わなければ pip が失敗して止まる。"""
    if not LOCK.exists():
        sys.exit(f"依存ロックが見つからない: {LOCK}")

    if not _venv_python():
        print(f"隔離環境を作成: {VENV}", file=sys.stderr)
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True)

    py = _venv_python()
    print("ロックから依存を導入（sha256 を検証）…", file=sys.stderr)
    subprocess.run(
        [str(py), "-m", "pip", "install",
         "--isolated",              # PIP_* 環境変数と pip.conf を無視する
         "--require-hashes",        # 全要件にハッシュ必須。1つでも欠ければ拒否
         "--only-binary", ":all:",  # sdist を拒否＝ビルド時の任意コード実行を防ぐ
         "--no-deps",               # ロックが依存の全体。解決で勝手に増やさない
         "--index-url", "https://pypi.org/simple",
         "--disable-pip-version-check",
         "-r", str(LOCK)],
        check=True,
    )


def _in_our_venv() -> bool:
    """すでに .venv の中で動いているか。

    .venv/bin/python は基底インタプリタへのシンボリックリンクなので、
    実行ファイルのパスを resolve して比べても区別できない。sys.prefix で見る。
    """
    return Path(sys.prefix).resolve() == VENV.resolve()


def _reexec_into_venv() -> None:
    """.venv の python で自分を起動し直す。"""
    py = _venv_python()
    if py is None or _in_our_venv() or os.environ.get(_REEXEC_GUARD):
        return
    os.environ[_REEXEC_GUARD] = "1"  # exec のループ防止
    os.execv(str(py), [str(py), str(Path(__file__).resolve()), *sys.argv[1:]])


def _bootstrap() -> None:
    if not _missing():
        return

    if "--install-deps" in sys.argv:
        _install_deps()

    _reexec_into_venv()  # .venv があるならそちらで動かし直す

    still = _missing()
    if not still:
        return

    sys.exit(textwrap.dedent(f"""\
        依存パッケージが不足している: {', '.join(still)}

        次のどちらかで導入する。

          1) 検証済みロックから隔離環境に入れる（推奨。システムのPythonは触らない）
               python3 {Path(__file__).name} --install-deps <他の引数…>

          2) 自分で環境を用意して入れる
               pip install -r {LOCK} \\
                   --require-hashes --only-binary :all: --no-deps \\
                   --index-url https://pypi.org/simple

        バージョンと sha256 は requirements.lock.txt に固定してある。
        更新は scripts/update_lock.py で行い、差分をレビューしてから取り込む。"""))


def _warn_version_drift() -> None:
    """ロックと違うバージョンで動いている場合に一度だけ知らせる。"""
    from importlib.metadata import PackageNotFoundError, version

    if not LOCK.exists():
        return

    pinned = {}
    for line in LOCK.read_text().splitlines():
        if line.startswith(("#", " ")) or "==" not in line:
            continue
        name, _, rest = line.partition("==")
        pinned[name.strip().lower()] = rest.split()[0].strip()

    drift = []
    for pkg in REQUIRED.values():
        try:
            got = version(pkg)
        except PackageNotFoundError:
            continue
        want = pinned.get(pkg.lower())
        if want and got != want:
            drift.append(f"{pkg} {got}（ロックは {want}）")
    if drift:
        print(f"警告: ロックと異なるバージョンで実行中: {', '.join(drift)}",
              file=sys.stderr)


_bootstrap()
_warn_version_drift()

from bs4 import BeautifulSoup  # noqa: E402
from pygments import highlight  # noqa: E402
from pygments.formatters import HtmlFormatter  # noqa: E402
from pygments.lexers import get_lexer_by_name, guess_lexer  # noqa: E402
from pygments.util import ClassNotFound  # noqa: E402
from weasyprint import HTML, CSS  # noqa: E402

# ---------------------------------------------------------------- 判型プリセット
# margin は 上 / 外(右) / 下 / 内(左)。外側マージンを広く取り側注を流し込む。
# sidenote_pull = sidenote_w + 逃げ。pull <= 外マージン に収める必要がある。
# 折り返さずに収まるコード1行の目安文字数（半角）。超えると自動折り返しになり
# 続き行が読みにくくなるため、ビルド時に警告を出す。
CODE_COLS = {"a4": 72, "b5": 60, "a5": 48}

PRESETS = {
    "a4": dict(size="210mm 297mm", height="297mm", margin="22mm 48mm 20mm 24mm",
               font="10.2pt", sidenote_w="34mm", sidenote_pull="40mm"),
    "b5": dict(size="182mm 257mm", height="257mm", margin="20mm 42mm 18mm 22mm",
               font="9.8pt", sidenote_w="30mm", sidenote_pull="35mm"),
    "a5": dict(size="148mm 210mm", height="210mm", margin="16mm 34mm 15mm 17mm",
               font="9.0pt", sidenote_w="24mm", sidenote_pull="28mm"),
}
# 側注を使わない場合の左右対称マージン
NARROW = {
    "a4": "22mm 26mm 20mm 26mm",
    "b5": "20mm 22mm 18mm 22mm",
    "a5": "16mm 18mm 15mm 18mm",
}

# ---------------------------------------------------------------- 索引の見出し分類

KANA_ROWS = [
    ("あ", "あぁいぃうぅえぇおぉ"),
    ("か", "かがきぎくぐけげこご"),
    ("さ", "さざしじすずせぜそぞ"),
    ("た", "ただちぢつっづてでとど"),
    ("な", "なにぬねの"),
    ("は", "はばぱひびぴふぶぷへべぺほぼぽ"),
    ("ま", "まみむめも"),
    ("や", "やゃゆゅよょ"),
    ("ら", "らりるれろ"),
    ("わ", "わをん"),
]


def to_hiragana(ch: str) -> str:
    """カタカナをひらがなに寄せる（索引の並び用）。"""
    code = ord(ch)
    if 0x30A1 <= code <= 0x30F6:
        return chr(code - 0x60)
    return ch


def index_group(term: str, yomi: str | None) -> tuple[int, str]:
    """索引エントリの見出しグループを返す。(並び順, 表示名)"""
    key = (yomi or term).strip()
    if not key:
        return (99, "その他")
    head = to_hiragana(key[0])
    if head.isascii() and head.isalpha():
        return (0, head.upper())
    for i, (label, chars) in enumerate(KANA_ROWS):
        if head in chars:
            return (10 + i, label)
    return (99, "その他")


def sort_key(term: str, yomi: str | None) -> str:
    key = (yomi or term).strip()
    return "".join(to_hiragana(c) for c in key).lower()

# ---------------------------------------------------------------- 各処理

def slugify(text: str, fallback: str) -> str:
    s = re.sub(r"[^\w\u3040-\u30ff\u4e00-\u9fff-]+", "-", text.strip().lower())
    s = s.strip("-")
    return s or fallback


def assign_heading_ids(soup: BeautifulSoup) -> None:
    """h1〜h3にIDを付ける。目次・相互参照のアンカーになる。"""
    seen: dict[str, int] = {}
    for i, h in enumerate(soup.find_all(["h1", "h2", "h3"])):
        if h.get("id"):
            continue
        base = slugify(h.get_text(), f"h-{i}")
        n = seen.get(base, 0)
        seen[base] = n + 1
        h["id"] = base if n == 0 else f"{base}-{n+1}"


def build_toc(soup: BeautifulSoup, depth: int) -> str:
    """章(.chapter h1) / 節(h2) / 項(h3) から目次のHTMLを組む。"""
    items = []
    for h in soup.find_all(["h1", "h2", "h3"]):
        # 表紙・索引・巻末解答の見出しは目次に載せない
        if h.find_parent(class_=["cover", "toc"]):
            continue
        lvl = int(h.name[1])
        if lvl > depth:
            continue
        cls = {1: "toc-ch", 2: "toc-sec", 3: "toc-sub"}[lvl]
        label = h.get_text(" ", strip=True)
        chap = h.find_parent(class_="chapter")
        if lvl == 1 and chap is not None:
            label = f"第{count_chapter_index(soup, chap)}章　{label}"
        items.append(
            f'<li class="{cls}"><a href="#{h["id"]}">{html.escape(label)}</a></li>'
        )
    if not items:
        return ""
    return (
        '<section class="frontmatter toc">\n<h1>目次</h1>\n<ul>\n'
        + "\n".join(items)
        + "\n</ul>\n</section>\n"
    )


def count_chapter_index(soup: BeautifulSoup, chapter_tag) -> int:
    chapters = soup.find_all(class_="chapter")
    return chapters.index(chapter_tag) + 1


def collect_index(soup: BeautifulSoup) -> str:
    """<span class="idx" data-term="..."> を集めて索引セクションを組む。"""
    entries: dict[str, dict] = {}
    for n, span in enumerate(soup.find_all(class_="idx")):
        term = (span.get("data-term") or span.get_text(strip=True)).strip()
        if not term:
            continue
        yomi = span.get("data-yomi")
        anchor = f"idx-{n}"
        span["id"] = anchor
        rec = entries.setdefault(term, {"yomi": yomi, "anchors": []})
        if yomi and not rec["yomi"]:
            rec["yomi"] = yomi
        rec["anchors"].append(anchor)

    if not entries:
        return ""

    grouped: dict[tuple[int, str], list] = {}
    for term, rec in entries.items():
        grouped.setdefault(index_group(term, rec["yomi"]), []).append((term, rec))

    parts = ['<section class="index">\n<h1>索引</h1>\n<div class="idx-cols">']
    for gkey in sorted(grouped):
        parts.append(f'<p class="idx-group">{html.escape(gkey[1])}</p>')
        rows = sorted(grouped[gkey], key=lambda t: sort_key(t[0], t[1]["yomi"]))
        for term, rec in rows:
            links = "".join(
                f'<a href="#{a}"></a>' for a in dict.fromkeys(rec["anchors"])
            )
            parts.append(
                f'<p class="idx-entry"><span class="idx-term">'
                f"{html.escape(term)}</span>{links}</p>"
            )
    parts.append("</div>\n</section>\n")
    return "\n".join(parts)


def highlight_code(soup: BeautifulSoup, max_cols: int) -> dict[str, str]:
    """<pre><code class="language-xxx"> をPygmentsで着色する。

    着色済みHTMLをsoupに差し戻すとBeautifulSoupが空白のみのテキストノードを
    捨ててしまい、コードのインデントが消える。そこでプレースホルダだけを置き、
    シリアライズ後に文字列として差し込む。
    """
    subs: dict[str, str] = {}
    for i, code in enumerate(soup.select("pre > code")):
        cls = " ".join(code.get("class") or [])
        m = re.search(r"(?:language|lang)-([\w+#.-]+)", cls)
        source = code.get_text()
        try:
            lexer = get_lexer_by_name(m.group(1)) if m else guess_lexer(source)
        except (ClassNotFound, ValueError):
            continue
        # linespans で1行=1spanにする。CSSで display:block にできるので、
        # 折り返した行にぶら下げインデントが効き、続き行だと一目で分かる。
        marked = highlight(source, lexer, HtmlFormatter(linespans=f"CL{i}"))
        marked = re.sub(r"^<div[^>]*><pre>(?:<span></span>)?", "", marked)
        marked = re.sub(r"</pre></div>\s*$", "", marked)
        marked = marked.replace("\n</span>", "</span>")          # 行末改行は不要
        marked = re.sub(r'(<span id="CL\d+-\d+">)</span>', r"\1&#160;</span>",
                        marked)                                   # 空行を潰さない
        long_lines = [
            (n, ln) for n, ln in enumerate(source.splitlines(), 1)
            if len(ln) > max_cols
        ]
        for n, ln in long_lines:
            print(f"warning: コード{i + 1}個目の{n}行目が{len(ln)}文字 "
                  f"(目安{max_cols}文字)。折り返されます: {ln[:40]}…",
                  file=sys.stderr)

        key = f"@@TECHBOOK-CODE-{i}@@"
        code.clear()
        code.append(key)
        subs[key] = marked.strip()
    return subs


def preset_css(args) -> str:
    p = PRESETS[args.preset]
    margin = p["margin"] if args.sidenotes else NARROW[args.preset]
    return f"""
@page {{
  size: {p['size']};
  margin: {margin};
}}
:root {{
  --accent: {args.accent};
  --accent-weak: {args.accent_weak};
  --page-h: {p['height']};
  --sidenote-w: {p['sidenote_w']};
  --sidenote-pull: -{p['sidenote_pull']};
}}
html {{ font-size: {p['font']}; }}
body {{ string-set: book-title "{args.title}"; }}
"""


def cover_html(args) -> str:
    if args.no_cover:
        return ""
    sub = (
        f'<p class="cover-sub">{html.escape(args.subtitle)}</p>'
        if args.subtitle else ""
    )
    author = (
        f'<p class="cover-author">{html.escape(args.author)}</p>'
        if args.author else ""
    )
    meta = (
        f'<p class="cover-meta">{html.escape(args.meta)}</p>'
        if args.meta else ""
    )
    kicker = (
        f'<p class="cover-kicker">{html.escape(args.kicker)}</p>'
        if args.kicker else ""
    )
    # 著者名も刊記も無い場合は下部ブロックごと落とす。
    # 罫線だけが取り残されると、情報が抜け落ちた表紙に見えてしまう。
    if author or meta:
        bottom = f"""  <div class="cover-bottom">
    <div class="cover-rule"></div>
    {author}
    {meta}
  </div>"""
        nofoot = ""
    else:
        bottom = ""
        nofoot = " nofoot"

    return f"""<section class="cover{nofoot}">
  <div class="cover-top">
    {kicker}
    <h1 class="cover-title">{html.escape(args.title)}</h1>
    {sub}
  </div>
{bottom}
</section>
"""

# ---------------------------------------------------------------- メイン

def main() -> int:
    ap = argparse.ArgumentParser(description="本文HTML断片から参考書PDFを作る")
    ap.add_argument("input", help="本文のHTML断片（<section class='chapter'>の並び）")
    ap.add_argument("-o", "--output", default="book.pdf")
    ap.add_argument("--preset", choices=list(PRESETS), default="b5")
    ap.add_argument("--title", default="無題")
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--author", default="", help="表紙の著者名。無ければ表紙下部ごと省かれる")
    ap.add_argument("--meta", default="", help="表紙下部の補足（版数・日付など）")
    ap.add_argument("--kicker", default="", help="表紙上部の小見出し")
    ap.add_argument("--accent", default="#1b4f8a")
    ap.add_argument("--accent-weak", default="#e8f0f9")
    ap.add_argument("--toc-depth", type=int, default=2, choices=[1, 2, 3])
    ap.add_argument("--no-cover", action="store_true")
    ap.add_argument("--no-toc", action="store_true")
    ap.add_argument("--no-index", action="store_true")
    ap.add_argument("--no-sidenotes", dest="sidenotes", action="store_false",
                    help="側注を使わない（左右対称の狭いマージンにする）")
    ap.add_argument("--keep-html", action="store_true")
    ap.add_argument("--install-deps", action="store_true",
                    help="不足依存を requirements.lock.txt から .venv に導入する"
                         "（sha256 検証あり。システムのPythonには入れない）")
    args = ap.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"error: 入力が見つかりません: {src}", file=sys.stderr)
        return 1

    body = BeautifulSoup(src.read_text(encoding="utf-8"), "html.parser")

    assign_heading_ids(body)
    code_subs = highlight_code(body, CODE_COLS[args.preset])
    # 索引は本文ツリーに組み込んでから目次を作る。
    # 別文字列のまま後ろに連結すると、目次に「索引」が載らない。
    index_section = "" if args.no_index else collect_index(body)
    if index_section:
        body.append(BeautifulSoup(index_section, "html.parser"))
        assign_heading_ids(body)      # 索引の見出しにもIDを振る

    toc_section = "" if args.no_toc else build_toc(body, args.toc_depth)

    rendered_body = body.decode()
    for key, marked in code_subs.items():
        rendered_body = rendered_body.replace(key, marked)

    skill_dir = Path(__file__).resolve().parent.parent
    book_css = (skill_dir / "templates" / "book.css").read_text(encoding="utf-8")
    pyg_css = HtmlFormatter(style="friendly").get_style_defs("pre")

    body_class = "" if args.sidenotes else "narrow-margins"

    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{html.escape(args.title)}</title>
<style>
{book_css}
{pyg_css}
{preset_css(args)}
</style>
</head>
<body class="{body_class}">
{cover_html(args)}
{toc_section}
{rendered_body}
</body>
</html>
"""

    out = Path(args.output)
    if args.keep_html:
        html_path = out.with_suffix(".html")
        html_path.write_text(doc, encoding="utf-8")
        print(f"中間HTML: {html_path}")

    HTML(string=doc, base_url=str(src.parent.resolve())).write_pdf(
        out, stylesheets=[CSS(string="")]
    )
    print(f"PDF出力: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
