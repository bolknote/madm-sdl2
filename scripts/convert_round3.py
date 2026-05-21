#!/usr/bin/env python3
"""Round-3 harvest: babyutils labeled asm, pico/tt RAM cross-check."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import (
    parse_asm_text,
    parse_babyutils_asm,
    parse_snp_text,
    to_signed32,
    write_store,
)

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
UP = SCRIPTS / "upstream"

PICO_C = UP / "pico-baby-if" / "pico-baby-if" / "program.c"
TT_TEST = UP / "tt-manchester-baby" / "tt-manchester-baby" / "test" / "test.py"
BABYUTILS_TEST = UP / "babyutils" / "babyutils" / "test"
COMPARCH_ASM = UP / "comparch" / "comparch" / "chapter07" / "TuringLongDivision.asm"
SIM_SAMPLES = UP / "bower-extra" / "manchester-baby-sim" / "samples" / "ssem"
MPY = UP / "bower-extra" / "ManchesterBabyPython"


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


def pico_words() -> list[int]:
    text = PICO_C.read_text()
    m = re.search(r"uint32_t program\[32\]\s*=\s*\{([^}]+)\}", text, re.S)
    if not m:
        raise ValueError("program[] missing")
    vals = [int(x.strip(), 0) for x in re.findall(r"0x[0-9a-fA-F]+", m.group(1))]
    return [to_signed32(v) for v in vals]


def tt_words() -> list[int]:
    text = TT_TEST.read_text()
    m = re.search(r"self\.program\s*=\s*\[(.*?)\]", text, re.S)
    if not m:
        raise ValueError("test.py program list missing")
    vals = [int(x.strip(), 0) for x in re.findall(r"0x[0-9a-fA-F]+", m.group(1))]
    return [to_signed32(v) for v in vals]


def has_code(words: list[int]) -> bool:
    return any(w != 0 for w in words)


def emit(name: str, title: str, url: str, words: list[int], ci: int | None) -> None:
    if not has_code(words):
        print("skip", name, "empty", file=sys.stderr)
        return
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def try_babyutils(path: Path) -> tuple[list[int], int | None] | None:
    try:
        words, ci = parse_babyutils_asm(path.read_text())
    except ValueError as e:
        print("skip", path.name, e, file=sys.stderr)
        return None
    if not has_code(words):
        print("skip", path.name, "empty", file=sys.stderr)
        return None
    return words, ci


def main() -> int:
    if PICO_C.is_file() and TT_TEST.is_file():
        pw, tw = pico_words(), tt_words()
        if pw != tw:
            print("warn: pico program.c != tt test.py RAM", file=sys.stderr)
        dup = same_as_catalog(pw)
        print(
            "pico/tt Turing long div:",
            "match catalog" if dup else "NEW",
            dup or "",
            "line28 init",
            hex(pw[28] & 0xFFFFFFFF),
            "(expect 0xe0000000 after run)",
        )

    if COMPARCH_ASM.is_file():
        try:
            w, ci = parse_asm_text(COMPARCH_ASM.read_text())
            emit(
                "comparch_turing_longdiv.store",
                "comparch ch07 — TuringLongDivision.asm",
                "https://gitlab.com/charles.fox/comparch/-/blob/main/chapter07/TuringLongDivision.asm",
                w,
                ci,
            )
        except ValueError as e:
            print("skip comparch", e, file=sys.stderr)

    if BABYUTILS_TEST.is_dir():
        for path in sorted(BABYUTILS_TEST.glob("*.asm")):
            r = try_babyutils(path)
            if not r:
                continue
            stem = path.stem.replace("-", "_")
            emit(
                f"babyutils_{stem}.store",
                f"babyutils — {path.name}",
                f"https://github.com/andy-bower/babyutils/blob/main/test/{path.name}",
                *r,
            )

    if SIM_SAMPLES.is_dir():
        for path in sorted(SIM_SAMPLES.glob("*.asm")):
            try:
                r = parse_asm_text(path.read_text())
            except ValueError:
                continue
            if r[0] and has_code(r[0]):
                emit(
                    f"bower_sim_{path.stem}.store",
                    f"manchester-baby-sim — {path.name}",
                    f"https://github.com/andy-bower/manchester-baby-sim/blob/main/samples/ssem/{path.name}",
                    *r,
                )

    for sub, label in (("Tests", "test"), ("Samples", "sample")):
        folder = MPY / sub
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.asm")):
            try:
                r = parse_asm_text(path.read_text())
            except ValueError:
                continue
            if r[0] and has_code(r[0]):
                emit(
                    f"bower_mpy_{path.stem.lower()}.store",
                    f"ManchesterBabyPython {label} — {path.name}",
                    f"https://github.com/andy-bower/ManchesterBabyPython/blob/main/{sub}/{path.name}",
                    *r,
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
