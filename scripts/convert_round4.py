#!/usr/bin/env python3
"""Round-4: BlackIce multiply, babyutils macro README, Linux Voice note."""

from __future__ import annotations

import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
BLACKICE_ASM = SCRIPTS / "upstream" / "blackice" / "multiply.asm"

# MADD2(x,y) = LDN x; SUB y; STO tmp; LDN tmp  (mneg)
MADD2_EXPANDED = """
01: LDN 7
02: SUB 8
03: STO 9
04: LDN 9
05: STO 10
06: STP
07: NUM 1
08: NUM 2
09: NUM 0
10: NUM 0
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


def emit(name: str, title: str, url: str, words: list[int], ci: int | None) -> None:
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def main() -> int:
    BLACKICE_ASM.write_text(
        """\
; BlackIce MX book — multiply lines 29×30 → 31 (MADM LSB-left store image)
; https://lawrie.github.io/blackicemxbook/Soft_Processors/Soft_Processors.html
; FPGA lines.hex uses different bit packing; this follows the book disassembly.

00: JMP 0
01: LDN 29
02: STO 25
03: LDN 25
04: STO 26
05: LDN 26
06: CMP 0
07: JMP 27
08: LDN 31
09: SUB 30
10: STO 25
11: LDN 25
12: STO 31
13: LDN 26
14: SUB 28
15: STO 25
16: LDN 25
17: STO 26
18: JMP 24
19: LDN 31
20: STO 25
21: LDN 25
22: STP 0
23: NUM 0
24: NUM 4
25: NUM 0
26: NUM 0
27: NUM 18
28: NUM -1
29: NUM 5
30: NUM 50
31: NUM 0
"""
    )
    words, ci = parse_asm_text(BLACKICE_ASM.read_text())
    emit(
        "blackice_multiply.store",
        "BlackIce MX book — multiply 5×50 (disassembly; not FPGA lines.hex bit order)",
        "https://lawrie.github.io/blackicemxbook/Soft_Processors/Soft_Processors.html",
        words,
        ci,
    )

    # README 1+2=3 with hand-expanded MADD2 (a=7, b=8, c=10, tmp=9)
    words2, ci2 = parse_asm_text(MADD2_EXPANDED)
    emit(
        "babyutils_madd2_readme.store",
        "babyutils README — MADD2 macro (1+2→3 in line 10)",
        "https://github.com/andy-bower/babyutils/blob/main/README.md",
        words2,
        ci2,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
