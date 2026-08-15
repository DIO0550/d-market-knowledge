#!/usr/bin/env python3
"""
requirements.lock.txt を再生成する保守用スクリプト（通常のビルドでは使わない）。

build_pdf.py の依存を pip に解決させ、確定した各バージョンについて
PyPI の JSON API から「そのバージョンに属する全ファイルの sha256」を取得して
ハッシュ付きロックを書き出す。

全ファイルのハッシュを列挙するのは、pip が --require-hashes 下で
「列挙されたどれか1つに一致すればOK」と判定するため。こうしておくと
ロックを作った環境（Linux / CPython 3.11）以外でも、その OS 向けの wheel が
そのまま検証を通る。1プラットフォームぶんだけ書くと他の環境で必ず失敗する。

使い方:
    python3 update_lock.py            # 更新して差分を書き出す
    python3 update_lock.py --check    # 更新せず、内容が最新かだけ確認する

更新したら必ず差分をレビューすること。バージョンが上がっている依存は
リリースノートを確認してから取り込む。ハッシュだけが変わっている場合は
PyPI 側の再アップロードを意味するので、取り込む前に事情を確認する。
"""

import argparse
import json
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

# build_pdf.py が直接 import するパッケージ。transitive な依存は pip が解決する。
DIRECT = ["weasyprint", "beautifulsoup4", "pygments"]

PYPI_JSON = "https://pypi.org/pypi/{name}/{version}/json"
LOCK = Path(__file__).resolve().parent / "requirements.lock.txt"

HEADER = """\
# techbook-pdf の依存ロック（自動生成 — 手で編集しない）
#
# 再生成:  python3 update_lock.py
# 検証:    python3 update_lock.py --check
#
# 各パッケージには、そのバージョンに属する全配布ファイルの sha256 を列挙している。
# pip は --require-hashes 下でいずれか1つに一致すれば受け入れるため、
# OS や Python バージョンが違ってもこのロックのまま検証が通る。
#
# インストールは build_pdf.py --install-deps 経由で行う（隔離環境に入る）。
# 手動で入れる場合:
#   pip install -r requirements.lock.txt \\
#       --require-hashes --only-binary :all: --no-deps \\
#       --index-url https://pypi.org/simple
"""


def resolve() -> list[tuple[str, str]]:
    """pip に依存を解決させ、(名前, バージョン) の一覧を返す。"""
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.json"
        subprocess.run(
            [sys.executable, "-m", "pip", "install",
             "--dry-run", "--ignore-installed", "--quiet",
             "--only-binary", ":all:",
             "--index-url", "https://pypi.org/simple",
             "--report", str(report), *DIRECT],
            check=True,
        )
        data = json.loads(report.read_text())

    pkgs = [(i["metadata"]["name"], i["metadata"]["version"]) for i in data["install"]]
    return sorted(pkgs, key=lambda p: p[0].lower())


def file_hashes(name: str, version: str) -> list[str]:
    """PyPI 上のそのバージョンの全ファイルの sha256 を返す。"""
    url = PYPI_JSON.format(name=name, version=version)
    with urllib.request.urlopen(url, timeout=60) as resp:
        data = json.load(resp)

    digests = sorted(
        {f["digests"]["sha256"] for f in data["urls"] if not f.get("yanked")}
    )
    if not digests:
        raise SystemExit(f"ハッシュを取得できない: {name}=={version}")
    return digests


def render(pkgs: list[tuple[str, str]]) -> str:
    out = [HEADER]
    for name, version in pkgs:
        digests = file_hashes(name, version)
        lines = [f"{name}=={version} \\"]
        lines += [f"    --hash=sha256:{d} \\" for d in digests]
        lines[-1] = lines[-1].rstrip(" \\")
        out.append("\n".join(lines))
    return "\n\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="書き換えず、ロックが最新かだけ確認する")
    args = ap.parse_args()

    print("依存を解決中…", file=sys.stderr)
    pkgs = resolve()
    print(f"  {len(pkgs)} パッケージ", file=sys.stderr)

    print("PyPI からハッシュを取得中…", file=sys.stderr)
    content = render(pkgs)

    if args.check:
        current = LOCK.read_text() if LOCK.exists() else ""
        if current == content:
            print("ロックは最新。", file=sys.stderr)
            return 0
        print("ロックが古い。python3 update_lock.py で再生成する。", file=sys.stderr)
        return 1

    LOCK.write_text(content)
    print(f"書き出した: {LOCK}", file=sys.stderr)
    for name, version in pkgs:
        print(f"  {name}=={version}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
