#!/usr/bin/env python3
"""Round-6: canonical reference/ sources → programs/*.store (+ upstream mirror)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, write_store
from convert_extra_hunt import rust_add5_store, rust_countdown_store

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
PROGRAMS = ROOT / "programs"
REF = ROOT / "reference"
UP = SCRIPTS / "upstream"

REF_FILES = [
    "rust_baby_emulator_countdown.asm",
    "blackice_multiply.asm",
    "blackice_multiply.lines.hex",
    "blackice_multiply.disasm",
    "mark_stevens_add.ssem",
    "mark_stevens_hfr989.ssem",
    "retro_factor_gobaby.asm",
]


def mirror_to_upstream() -> None:
    """Copy tracked reference/ into gitignored upstream cache."""
    for name in REF_FILES:
        src = REF / name
        if not src.is_file():
            continue
        if name.startswith("blackice"):
            dst = UP / "blackice" / name.replace("blackice_multiply.", "blackice_multiply.")
            if name == "blackice_multiply.asm":
                dst = UP / "blackice" / "multiply.asm"
            else:
                dst = UP / "blackice" / name
        elif name.startswith("mark_stevens"):
            dst = UP / "mark-stevens" / name.replace("mark_stevens_", "")
        elif name.startswith("rust"):
            dst = UP / "baby-rust" / name
        elif name.startswith("retro"):
            dst = UP / "retro-factor" / "factor.asm"
        else:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def refresh_catalog_stores() -> None:
    write_store(
        PROGRAMS / "baby_rust_countdown.store",
        "baby-emulator — count 10 down via CMP/JMP loop (README ASM)",
        "reference/rust_baby_emulator_countdown.asm",
        rust_countdown_store(),
        ci_start=-1,
    )
    print("wrote baby_rust_countdown.store")

    write_store(
        PROGRAMS / "baby_rust_add5.store",
        "baby-emulator — new_example_program (5+5 in accumulator)",
        "https://docs.rs/baby-emulator/0.2.1/baby_emulator/core/struct.BabyModel.html#method.new_example_program",
        rust_add5_store(),
        ci_start=-1,
    )
    print("wrote baby_rust_add5.store")

    blackice = REF / "blackice_multiply.asm"
    if blackice.is_file():
        words, ci = parse_asm_text(blackice.read_text())
        write_store(
            PROGRAMS / "blackice_multiply.store",
            "BlackIce MX book — multiply 5×50 (MADM LSB-left)",
            "reference/blackice_multiply.asm",
            words,
            ci_start=ci,
        )
        print("wrote blackice_multiply.store")

    add = REF / "mark_stevens_add.ssem"
    if add.is_file():
        words, ci = parse_asm_text(add.read_text())
        write_store(
            PROGRAMS / "nevynuk_add.store",
            "Mark Stevens / NevynUK — 10 + 5 → 15 in accumulator",
            "reference/mark_stevens_add.ssem",
            words,
            ci_start=ci,
        )
        print("wrote nevynuk_add.store")

    hfr = REF / "mark_stevens_hfr989.ssem"
    if hfr.is_file():
        words, ci = parse_asm_text(hfr.read_text())
        write_store(
            PROGRAMS / "nevynuk_hcf989.store",
            "Mark Stevens / NevynUK — HCF for 989",
            "reference/mark_stevens_hfr989.ssem",
            words,
            ci_start=ci,
        )
        print("wrote nevynuk_hcf989.store")

    retro = REF / "retro_factor_gobaby.asm"
    if retro.is_file():
        words, ci = parse_asm_text(retro.read_text())
        write_store(
            PROGRAMS / "gobaby_factor.store",
            "gobaby factor 2^18 — Retro SE / gobaby examples/factor.asm",
            "reference/retro_factor_gobaby.asm",
            words,
            ci_start=ci,
        )
        print("wrote gobaby_factor.store")


def main() -> int:
    missing = [n for n in REF_FILES if not (REF / n).is_file()]
    if missing:
        print("missing reference/", ", ".join(missing), file=sys.stderr)
        return 1
    mirror_to_upstream()
    refresh_catalog_stores()
    print("mirrored reference/ → scripts/upstream/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
