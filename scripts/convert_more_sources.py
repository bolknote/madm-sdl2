#!/usr/bin/env python3
"""BabyPing (6× .ssem), gobaby .asm — write .store only when bytes differ from catalog."""

from __future__ import annotations

import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, write_store
from convert_extra_hunt import babyping_bits_to_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
BABYPING = SCRIPTS / "upstream" / "babyping" / "babyping" / "programs"
GOBABY = SCRIPTS / "upstream" / "gobaby" / "gobaby" / "examples"
GOBABY_URL = "https://github.com/jcla1/gobaby"


def load_store_words(path: Path) -> list[int]:
    words = [0] * 32
    for raw in path.read_text().splitlines():
        if raw.startswith("@"):
            parts = raw.split()
            words[int(parts[0][1:])] = int(parts[1], 0)
    return words


def same_as_existing(words: list[int]) -> str | None:
    for path in sorted(PROGRAMS.glob("*.store")):
        if path.name.startswith("babyping_") or path.name.startswith("gobaby_"):
            continue
        if load_store_words(path) == words:
            return path.name
    return None


def main() -> int:
    if not BABYPING.is_dir():
        print("missing", BABYPING, file=sys.stderr)
        return 1

    babyping = [
        ("clock.ssem", "babyping_clock.store", "CRT clock display"),
        ("intdiv.ssem", "babyping_intdiv.store", "Integer division"),
        ("kilburn.ssem", "babyping_kilburn.store", "Highest-factor (Kilburn-style bit dump)"),
        ("noodle.ssem", "babyping_noodle.store", "Three-minute noodle timer"),
        ("parabola.ssem", "babyping_parabola.store", "Parabola / difference-equation plot"),
        ("scroll.ssem", "babyping_scroll.store", "Scrolling CRT pattern"),
    ]
    for src, dst, title in babyping:
        path = BABYPING / src
        if not path.is_file():
            print("skip missing", src, file=sys.stderr)
            continue
        words = babyping_bits_to_store(path)
        dup = same_as_existing(words)
        write_store(
            PROGRAMS / dst,
            f"BabyPing — {title}"
            + (f" (same bytes as {dup})" if dup else ""),
            f"https://github.com/hrvach/babyping/blob/main/programs/{src}",
            words,
            ci_start=-1,
        )
        print("wrote", dst, f"(dup {dup})" if dup else "(unique)")

    if GOBABY.is_dir():
        for asm, dst, title in [
            ("factor.asm", "gobaby_factor.store", "Original factor program (2^18)"),
            ("primegen.asm", "gobaby_primegen.store", "Successive prime generator (chainable)"),
            ("simple_calc.asm", "gobaby_simple_calc.store", "Simple calculator demo"),
        ]:
            path = GOBABY / asm
            if not path.is_file():
                continue
            words, ci = parse_asm_text(path.read_text())
            dup = same_as_existing(words)
            write_store(
                PROGRAMS / dst,
                f"gobaby — {title}" + (f" (same bytes as {dup})" if dup else ""),
                f"{GOBABY_URL}/blob/main/examples/{asm}",
                words,
                ci_start=ci,
            )
            print("wrote", dst, f"(dup {dup})" if dup else "")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
