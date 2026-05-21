#!/usr/bin/env python3
"""Round-2 sources: babyutils, comparch ch07, Bower sim/Python (labeled asm skipped)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, parse_snp_text, to_signed32, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
UP = SCRIPTS / "upstream"

PICO_C = UP / "pico-baby-if" / "pico-baby-if" / "program.c"
COMPARCH_ASM = UP / "comparch" / "comparch" / "chapter07" / "TuringLongDivision.asm"
BABYUTILS_TEST = UP / "babyutils" / "babyutils" / "test"
SIM_SAMPLES = UP / "bower-extra" / "manchester-baby-sim" / "samples" / "ssem"
MPY_TESTS = UP / "bower-extra" / "ManchesterBabyPython" / "Tests"
MPY_SAMPLES = UP / "bower-extra" / "ManchesterBabyPython" / "Samples"

OP_MASK = 0x1F << 13


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


def has_code(words: list[int]) -> bool:
    return any(w != 0 for w in words)


def pico_program_c() -> list[int]:
    text = PICO_C.read_text()
    m = re.search(r"uint32_t program\[32\]\s*=\s*\{([^}]+)\}", text, re.S)
    if not m:
        raise ValueError("program[] not found in program.c")
    vals = [int(x.strip(), 0) for x in re.findall(r"0x[0-9a-fA-F]+", m.group(1))]
    if len(vals) != 32:
        raise ValueError(f"expected 32 words, got {len(vals)}")
    return [to_signed32(v) for v in vals]


def try_asm(path: Path) -> tuple[list[int], int | None] | None:
    try:
        words, ci = parse_asm_text(path.read_text())
    except ValueError as e:
        print("skip asm", path.name, e, file=sys.stderr)
        return None
    if not has_code(words):
        print("skip asm", path.name, "no resolved words (labels/EJA?)", file=sys.stderr)
        return None
    return words, ci


def emit(name: str, title: str, url: str, words: list[int], ci: int | None) -> None:
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"same bytes as {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def main() -> int:
    if PICO_C.is_file():
        emit(
            "pico_turing_longdiv.store",
            "pico-baby-if — Turing long division (program.c)",
            "https://github.com/krisjdev/pico-baby-if/blob/main/program.c",
            pico_program_c(),
            -1,
        )

    if COMPARCH_ASM.is_file():
        r = try_asm(COMPARCH_ASM)
        if r:
            emit(
                "comparch_turing_longdiv.store",
                "comparch ch07 — TuringLongDivision.asm",
                "https://gitlab.com/charles.fox/comparch/-/blob/main/chapter07/TuringLongDivision.asm",
                *r,
            )

    if BABYUTILS_TEST.is_dir():
        for path in sorted(BABYUTILS_TEST.glob("*.asm")):
            if path.name.endswith("-pic.asm"):
                continue
            r = try_asm(path)
            if r:
                stem = path.stem.replace("-", "_")
                emit(
                    f"babyutils_{stem}.store",
                    f"babyutils test — {path.name}",
                    f"https://github.com/andy-bower/babyutils/blob/main/test/{path.name}",
                    *r,
                )

    if SIM_SAMPLES.is_dir():
        for path in sorted(SIM_SAMPLES.glob("*.asm")):
            r = try_asm(path)
            if r:
                emit(
                    f"bower_sim_{path.stem}.store",
                    f"manchester-baby-sim — {path.name}",
                    f"https://github.com/andy-bower/manchester-baby-sim/blob/main/samples/ssem/{path.name}",
                    *r,
                )
        snp_dir = SIM_SAMPLES / "tests"
        if snp_dir.is_dir():
            for path in sorted(snp_dir.glob("*.snp")):
                words, ci = parse_snp_text(path.read_text())
                if not has_code(words):
                    continue
                stem = path.stem.lower().replace("test", "")
                emit(
                    f"bower_sim_{stem}.store",
                    f"manchester-baby-sim — {path.name}",
                    f"https://github.com/andy-bower/manchester-baby-sim/blob/main/samples/ssem/tests/{path.name}",
                    words,
                    ci,
                )

    for folder, prefix, base_url in (
        (MPY_TESTS, "bower_mpy", "Tests"),
        (MPY_SAMPLES, "bower_mpy", "Samples"),
    ):
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.asm")):
            r = try_asm(path)
            if r:
                emit(
                    f"{prefix}_{path.stem.lower()}.store",
                    f"ManchesterBabyPython {base_url.lower()} — {path.name}",
                    f"https://github.com/andy-bower/ManchesterBabyPython/blob/main/{base_url}/{path.name}",
                    *r,
                )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
