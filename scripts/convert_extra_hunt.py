#!/usr/bin/env python3
"""BabyPing bit dumps, Rust baby-emulator examples, CCS PROG1 (989)."""

from __future__ import annotations

import sys
from pathlib import Path

from convert_baby_source import bits_to_word, enc, to_signed32, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
BABYPING = SCRIPTS / "upstream" / "babyping" / "babyping" / "programs"
FACTORCT = PROGRAMS / "ccs_factorct.store"
CCS_URL = (
    "https://computerconservationsociety.org/ssemvolunteers/volunteers/"
    "A%20Technical%20Introduction%20To%20Programming%20the%20Baby%20v4.0.pdf"
)


def babyping_bits_to_store(path: Path) -> list[int]:
    store = [0] * 32
    for i, line in enumerate(path.read_text().splitlines()):
        bits = line.strip()
        if len(bits) == 32 and set(bits) <= {"0", "1"}:
            store[i] = bits_to_word(bits)
    return store


def rust_add5_store() -> list[int]:
    """baby_emulator::BabyModel::new_example_program() layout."""
    return [
        enc(2, 5),
        enc(4, 5),
        enc(3, 6),
        enc(2, 6),
        enc(7, 0),
        to_signed32(-5),
        *([0] * 26),
    ]


def rust_countdown_store() -> list[int]:
    """COUNTDOWN_ASM from SSEMBabyEmulator docs; JMP via store line holding CI=0 (MADM loop @1)."""
    return [
        enc(2, 7),
        enc(4, 6),
        enc(6, 0),
        enc(0, 5),
        enc(7, 0),
        0,
        to_signed32(1),
        to_signed32(-10),
        *([0] * 24),
    ]


def prog1_from_factorct() -> list[int]:
    store = [0] * 32
    for raw in FACTORCT.read_text().splitlines():
        if raw.startswith("@"):
            parts = raw.split()
            store[int(parts[0][1:])] = int(parts[1], 0)
    store[23] = to_signed32(-989)
    store[24] = to_signed32(988)
    return store


def main() -> int:
    if not BABYPING.is_dir():
        print("missing", BABYPING, file=sys.stderr)
        return 1

    write_store(
        PROGRAMS / "baby_rust_add5.store",
        "baby-emulator — new_example_program (5+5 in accumulator)",
        "https://docs.rs/baby-emulator/0.2.1/baby_emulator/core/struct.BabyModel.html#method.new_example_program",
        rust_add5_store(),
        ci_start=-1,
    )
    print("wrote baby_rust_add5.store")

    write_store(
        PROGRAMS / "baby_rust_countdown.store",
        "baby-emulator — count 10 down via CMP/JMP loop (README ASM example)",
        "https://github.com/jasonalexander-ja/SSEMBabyEmulator",
        rust_countdown_store(),
        ci_start=-1,
    )
    print("wrote baby_rust_countdown.store")

    if FACTORCT.is_file():
        write_store(
            PROGRAMS / "ccs_prog1_989.store",
            "CCS guide — PROG1.SNP layout (factor 989 → answer in line 27)",
            CCS_URL,
            prog1_from_factorct(),
            ci_start=-1,
        )
        print("wrote ccs_prog1_989.store")

    babyping_meta = [
        ("scroll.ssem", "babyping_scroll.store", "BabyPing — scrolling CRT pattern"),
        ("kilburn.ssem", "babyping_kilburn.store", "BabyPing — factor program (bit dump)"),
    ]
    for src, dst, title in babyping_meta:
        path = BABYPING / src
        if not path.is_file():
            continue
        write_store(
            PROGRAMS / dst,
            title,
            "https://github.com/hrvach/babyping",
            babyping_bits_to_store(path),
            ci_start=-1,
        )
        print("wrote", dst)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
