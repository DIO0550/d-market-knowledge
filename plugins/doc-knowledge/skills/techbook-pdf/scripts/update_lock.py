#!/usr/bin/env python3
"""
requirements.lock.txt を再生成する保守用スクリプト。

**ロックは固定運用で、定期的に更新しない。** 通常のビルドでは使わないし、
上流に新しい版が出たというだけでは実行しない。脆弱性・悪性パッケージの報告が出た、
必要な修正が新版に入っている、新しい Python でビルドが通らない、といった
理由があるときだけ実行する（--check が「古い」と言うのは更新の理由にならない）。

build_pdf.py の依存を pip に解決させ、確定した各バージョンについて
PyPI の JSON API から「そのバージョンに属する全ファイルの sha256」を取得して
ハッシュ付きロックを書き出す。

全ファイルのハッシュを列挙するのは、pip が --require-hashes 下で
「列挙されたどれか1つに一致すればOK」と判定するため。こうしておくと
ロックを作った環境（Linux / CPython 3.11）以外でも、その OS 向けの wheel が
そのまま検証を通る。1プラットフォームぶんだけ書くと他の環境で必ず失敗する。

公開直後のバージョンは選ばない。最新版を掴むと、リリースが乗っ取られていた場合に
それが発覚する前の窓で取り込んでしまう（実際に起きている攻撃の典型例）。
既定で公開から MIN_AGE_DAYS 日を過ぎた版の中で最も新しいものを選ぶ。

使い方:
    python3 update_lock.py            # 更新して差分を書き出す
    python3 update_lock.py --check    # 更新せず、内容が最新かだけ確認する
    python3 update_lock.py --min-age 30

更新したら必ず差分をレビューすること。バージョンが上がっている依存は
リリースノートを確認してから取り込む。ハッシュだけが変わっている場合は
PyPI 側の再アップロードを意味するので、取り込む前に事情を確認する。
長く更新の無かったパッケージが突然リリースされている場合は特に警戒する
（メンテナのアカウント乗っ取りでよく見られる兆候）。
"""

import argparse
import json
import subprocess
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from packaging.version import InvalidVersion, Version

# build_pdf.py が直接 import するパッケージ。transitive な依存は pip が解決する。
DIRECT = ["weasyprint", "beautifulsoup4", "pygments"]

# 公開からこの日数を過ぎたバージョンだけを候補にする。
MIN_AGE_DAYS = 14

PYPI_JSON = "https://pypi.org/pypi/{name}/{version}/json"
PYPI_ALL = "https://pypi.org/pypi/{name}/json"
LOCK = Path(__file__).resolve().parent / "requirements.lock.txt"

_cache: dict[str, dict] = {}


def _pypi(url: str) -> dict:
    if url not in _cache:
        with urllib.request.urlopen(url, timeout=60) as resp:
            _cache[url] = json.load(resp)
    return _cache[url]


def _age_days(uploaded: str) -> float:
    ts = datetime.fromisoformat(uploaded.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - ts).total_seconds() / 86400


def age_of(name: str, version: str) -> float:
    """そのバージョンが公開されてからの日数。"""
    urls = _pypi(PYPI_JSON.format(name=name, version=version))["urls"]
    if not urls:
        return 0.0
    return _age_days(min(u["upload_time_iso_8601"] for u in urls))


def newest_aged(name: str, min_age: float) -> str:
    """min_age 日以上経っているバージョンのうち最も新しいものを返す。"""
    releases = _pypi(PYPI_ALL.format(name=name))["releases"]
    ok = []
    for ver, files in releases.items():
        files = [f for f in files if not f.get("yanked")]
        if not files:
            continue
        try:
            parsed = Version(ver)
        except InvalidVersion:
            continue
        if parsed.is_prerelease or parsed.is_devrelease:
            continue
        if _age_days(min(f["upload_time_iso_8601"] for f in files)) >= min_age:
            ok.append((parsed, ver))
    if not ok:
        raise SystemExit(f"{name}: {min_age}日以上経過した版が無い")
    return max(ok)[1]

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


def resolve(constraints: dict[str, str]) -> list[tuple[str, str]]:
    """pip に依存を解決させ、(名前, バージョン) の一覧を返す。

    constraints は {パッケージ名: 上限バージョン}。依存関係の解決自体は pip に任せ、
    こちらは「これより新しい版は使うな」という上限だけを渡す。
    """
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.json"
        cmd = [sys.executable, "-m", "pip", "install",
               "--dry-run", "--ignore-installed", "--quiet",
               "--only-binary", ":all:",
               "--index-url", "https://pypi.org/simple",
               "--report", str(report)]
        if constraints:
            cfile = Path(tmp) / "constraints.txt"
            cfile.write_text(
                "\n".join(f"{n}<={v}" for n, v in sorted(constraints.items())) + "\n"
            )
            cmd += ["--constraint", str(cfile)]
        subprocess.run(cmd + DIRECT, check=True)
        data = json.loads(report.read_text())

    pkgs = [(i["metadata"]["name"], i["metadata"]["version"]) for i in data["install"]]
    return sorted(pkgs, key=lambda p: p[0].lower())


def resolve_aged(min_age: float) -> list[tuple[str, str]]:
    """公開から min_age 日を過ぎた版だけで依存を解決する。

    解決自体は pip に任せ、期間を満たさない版が選ばれたらその上限を足して
    解決し直す、を落ち着くまで繰り返す。
    """
    constraints: dict[str, str] = {}
    for _ in range(10):
        pkgs = resolve(constraints)
        fresh = [(n, v) for n, v in pkgs if age_of(n, v) < min_age]
        if not fresh:
            return pkgs
        for name, version in fresh:
            allowed = newest_aged(name, min_age)
            print(f"  {name} {version} は公開 {age_of(name, version):.1f} 日 "
                  f"→ {allowed} に下げる", file=sys.stderr)
            constraints[name] = allowed
    raise SystemExit("バージョンの選び直しが収束しない。手で確認する。")


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
    ap.add_argument("--min-age", type=float, default=MIN_AGE_DAYS,
                    help=f"採用する版の最低経過日数（既定 {MIN_AGE_DAYS}）")
    args = ap.parse_args()

    print(f"依存を解決中（公開から{args.min_age:g}日以上経った版のみ）…", file=sys.stderr)
    pkgs = resolve_aged(args.min_age)
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
