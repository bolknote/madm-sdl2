#!/usr/bin/env python3
"""Layer-8 harvest: Madrona SSEM, Computer50 ssemref, HASE mirror check."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, write_store

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
REFERENCE = ROOT / "reference"
PROGRAMS = ROOT / "programs"
UP = SCRIPTS / "upstream"

MADRONA_PROG = UP / "madrona-ssem" / "programs"
SSEMREF = UP / "manchester-ref" / "ssemref.html"
HASE_DIR = UP / "hase" / "mu_baby-4.1"

SSEMREF_ADD_XY = """
; Computer50 SSEM Programmer's Reference Manual — Appendix A2.1
; Addition via SUB (x=5, y=3 → result in line 30)
3: LDN 28
4: SUB 29
5: STO 30
6: LDN 30
7: STO 30
28: NUM 5
29: NUM 3
30: NUM 0
"""

SSEMREF_SMALL_LOOP = """
; A2.2 fragment — decrement-until-negative using line 20 as constant 1 and JMP target 2
1: LDN 31
2: STO 29
3: LDN 29
4: SUB 20
5: SKN
6: JMP 20
7: HLT
20: NUM 1
28: NUM 2
31: NUM 7
"""

SSEMREF_IDX_MOD = """
; A2.3 fragment — instruction modification (not a complete runnable program)
6: SUB 19
12: LDN 6
13: STO 0
14: LDN 0
15: SUB 18
16: STO 6
17: JMP 0
18: NUM -1
"""


def load_store_words(path: Path) -> list[int]:
    words = [0] * 32
    for raw in path.read_text().splitlines():
        if raw.startswith("@"):
            parts = raw.split()
            words[int(parts[0][1:])] = int(parts[1], 0)
    return words


def same_as_catalog(words: list[int]) -> str | None:
    for path in sorted(PROGRAMS.glob("*.store")):
        if load_store_words(path) == words:
            return path.name
    return None


def extract_pre(html: str) -> str:
    m = re.search(r"<pre>(.*?)</pre>", html, re.S | re.I)
    return m.group(1) if m else ""


def emit(name: str, title: str, url: str, words: list[int], ci: int | None) -> None:
    if not any(words):
        print("skip", name, "empty", file=sys.stderr)
        return
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def sync_madrona_html() -> None:
    ref = REFERENCE / "madrona" / "programs"
    ref.mkdir(parents=True, exist_ok=True)
    if not MADRONA_PROG.is_dir():
        print("warn: missing", MADRONA_PROG, file=sys.stderr)
        return
    for src in sorted(MADRONA_PROG.glob("*.html")):
        shutil.copy2(src, ref / src.name)
    print("mirrored", len(list(ref.glob("*.html"))), "Madrona HTML pages")


def madrona_stores() -> None:
    if not MADRONA_PROG.is_dir():
        return
    base = "https://madrona.ca/e/SSEM/programs/"
    for html in sorted(MADRONA_PROG.glob("*.html")):
        if html.name == "index.html":
            continue
        pre = extract_pre(html.read_text())
        if not pre.strip():
            continue
        try:
            words, ci = parse_asm_text(pre)
        except Exception as exc:
            print("madrona", html.stem, "parse fail:", exc, file=sys.stderr)
            continue
        stem = html.stem
        if stem in ("medclock", "noodle", "sqrt"):
            emit(
                f"madrona_{stem}.store" if stem != "noodle" else "madrona_noodletimer.store",
                f"Madrona SSEM — {stem} (simulator preload)",
                base + html.name,
                words,
                ci,
            )


def ssemref_refs() -> None:
    ref = REFERENCE / "manchester-ref"
    ref.mkdir(parents=True, exist_ok=True)
    if SSEMREF.is_file():
        shutil.copy2(SSEMREF, ref / "ssemref.html")
    (ref / "add_xy_pattern.asm").write_text(SSEMREF_ADD_XY.strip() + "\n", encoding="utf-8")
    (ref / "small_constant_loop.asm").write_text(SSEMREF_SMALL_LOOP.strip() + "\n", encoding="utf-8")
    (ref / "instruction_modification_pattern.asm").write_text(
        SSEMREF_IDX_MOD.strip() + "\n", encoding="utf-8"
    )
    print("wrote manchester-ref/*.asm")

    words, ci = parse_asm_text(SSEMREF_ADD_XY)
    emit(
        "manchester_ref_add_xy.store",
        "Computer50 ssemref A2.1 — add x+y via SUB (lines 28–30)",
        "https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/prog98/ssemref.html#A2.1",
        words,
        ci,
    )
    words2, ci2 = parse_asm_text(SSEMREF_SMALL_LOOP)
    emit(
        "manchester_ref_dec_loop_a22.store",
        "Computer50 ssemref A2.2 — decrement loop (JMP via line 20)",
        "https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/prog98/ssemref.html#A2.2",
        words2,
        ci2,
    )


def hase_mirror_note() -> None:
    dst = REFERENCE / "hase_mirror_note.md"
    lines = [
        "# HASE mu_baby mirrors",
        "",
        "Primary cache: `scripts/upstream/hase/mu_baby_v4.1.zip` → `mu_baby-4.1/`.",
        "Catalog: `hase_insn_demo`, `hase_highest_factor`, `hase_third_demo` via `convert_program_hunt.py`.",
        "",
    ]
    if HASE_DIR.is_dir():
        lines.append("INPUT files present; no second unique program image found in layer 8.")
    else:
        lines.append("Unzip HASE zip after `./download_upstream.sh`.")
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", dst.relative_to(ROOT))


def main() -> int:
    sync_madrona_html()
    madrona_stores()
    ssemref_refs()
    hase_mirror_note()
    print("Layer 8 done — see reference/LAYER8_HARVEST.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
