#!/usr/bin/env python3
"""Build nevynuk_*.store from NevynUK/ManchesterBaby Source/SSEMPrograms/*.ssem."""

from __future__ import annotations

import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
SSEM_DIR = SCRIPTS / "upstream" / "nevynuk" / "ManchesterBaby" / "Source" / "SSEMPrograms"
REPO_URL = "https://github.com/NevynUK/ManchesterBaby"

PROGRAMS_META: list[tuple[str, str, str]] = [
    ("Add.ssem", "nevynuk_add.store", "Add two numbers (10 + 5 → line 22)"),
    ("HCF1.ssem", "nevynuk_hcf1.store", "Highest factor demo (number −35 in line 23)"),
    ("HCF2.ssem", "nevynuk_hcf2.store", "Euclidean HCF (large A/B in lines 30–31)"),
    ("hfr989.ssem", "nevynuk_hcf989.store", "HCF for 989 (Mark Stevens blog listing)"),
    (
        "TuringLongDivision.ssem",
        "nevynuk_turing_longdiv.store",
        "Alan Turing long division (36÷5 example; quotient in line 28)",
    ),
    ("Factor95.ssem", "nevynuk_jmp_test.store", "JMP instruction test (not factorization)"),
    ("Primes.ssem", "nevynuk_primes.store", "Prime generator"),
    ("Parabola.ssem", "nevynuk_parabola.store", "Parabola / difference-equation plot"),
    ("Nightmare.ssem", "nevynuk_nightmare.store", "Nightmare animation"),
    ("IntDivision.ssem", "nevynuk_intdiv.store", "Integer division"),
    ("Clock.ssem", "nevynuk_clock.store", "Clock display"),
    ("3Minutes.ssem", "nevynuk_3minutes.store", "Three-minute timer"),
]


def main() -> int:
    if not SSEM_DIR.is_dir():
        print(
            "missing",
            SSEM_DIR,
            "— clone https://github.com/NevynUK/ManchesterBaby under scripts/upstream/nevynuk/",
            file=sys.stderr,
        )
        return 1

    for src_name, out_name, title in PROGRAMS_META:
        path = SSEM_DIR / src_name
        if not path.is_file():
            print("skip missing", path.name, file=sys.stderr)
            continue
        store, ci = parse_asm_text(path.read_text())
        write_store(
            PROGRAMS / out_name,
            f"NevynUK — {title}",
            f"{REPO_URL}/blob/main/Source/SSEMPrograms/{src_name}",
            store,
            ci_start=ci,
        )
        print("wrote", out_name)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
