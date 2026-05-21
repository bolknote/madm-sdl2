#!/usr/bin/env python3
"""CCS wmadm.zip .mdm store images (LSB-left binary, S: section)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import bits_to_word, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
WMADM = SCRIPTS / "upstream" / "ccs-emu" / "wmadm_unpack"


def parse_mdm_text(text: str) -> tuple[list[int], int | None]:
    store = [0] * 32
    section: str | None = None
    s_idx = 0
    for raw in text.splitlines():
        line = raw.split("#")[0].strip()
        if not line:
            continue
        if line.endswith(":"):
            tag = line[:-1].upper()
            m = re.match(r"^S(\d+)$", tag)
            if m:
                s_idx = int(m.group(1))
                section = "S"
            else:
                section = tag
                if section == "S":
                    s_idx = 0
            continue
        if section == "S" and s_idx < 32:
            bits = line.replace(" ", "")
            if not bits or not set(bits) <= {"0", "1"}:
                continue
            if len(bits) < 32:
                bits = bits.ljust(32, "0")
            store[s_idx] = bits_to_word(bits[:32])
            s_idx += 1
    ci = -1 if store[1] else None
    return store, ci


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


def main() -> int:
    factor = WMADM / "factor.mdm"
    if not factor.is_file():
        print("missing", factor, "— unzip wmadm.zip under scripts/upstream/ccs-emu/", file=sys.stderr)
        return 1
    words, ci = parse_mdm_text(factor.read_text())
    dup = same_as_catalog(words)
    if dup:
        print("wmadm factor.mdm", "dup", dup, file=sys.stderr)
        return 0
    write_store(
        PROGRAMS / "wmadm_factor_july48.store",
        "CCS wmadm — Kilburn highest-factor (.mdm, 18 July 1948)",
        "https://www.computerconservationsociety.org/software/ssem/wmadm.zip",
        words,
        ci_start=ci,
    )
    print("wrote wmadm_factor_july48.store")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
