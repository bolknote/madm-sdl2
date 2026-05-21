#!/usr/bin/env python3
"""BabyBaby FPGA Programs.coe / BabySlide.coe → .store (LSB-left bit strings)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import bits_to_word, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
BB = SCRIPTS / "upstream" / "babybaby" / "BabyBaby" / "ipcore_dir"
PROGRAMS_COE = BB / "Programs.coe"
REPO = "https://github.com/g4ugm/BabyBaby"


def parse_coe_words(path: Path, start: int = 0, count: int = 32) -> list[int]:
    bits: list[str] = []
    in_vec = False
    for raw in path.read_text().splitlines():
        line = raw.strip().rstrip(",").rstrip(";")
        if "memory_initialization_vector" in line:
            in_vec = True
            continue
        if not in_vec or not line or line.startswith(";"):
            continue
        bits.append(line)
    if len(bits) < start + count:
        raise ValueError(f"{path}: need {start + count} lines, got {len(bits)}")
    return [bits_to_word(b) for b in bits[start : start + count]]


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


def emit(name: str, title: str, url: str, words: list[int], ci: int = -1) -> None:
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def main() -> int:
    if not PROGRAMS_COE.is_file():
        print("missing", PROGRAMS_COE, file=sys.stderr)
        return 1

    blocks = [
        (
            "babybaby_slider_baby.store",
            "BabyBaby — Slider with “BABY” bitmap (lines 21–27)",
            0,
        ),
        (
            "babybaby_primegen.store",
            "BabyBaby — PrimeGen (Programs.coe bank 2)",
            32,
        ),
        (
            "babybaby_diffeqt.store",
            "BabyBaby — Diffeq / parabola (Programs.coe bank 3)",
            64,
        ),
    ]
    for out, title, start in blocks:
        words = parse_coe_words(PROGRAMS_COE, start)
        emit(
            out,
            title,
            f"{REPO}/blob/master/ipcore_dir/Programs.coe",
            words,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
