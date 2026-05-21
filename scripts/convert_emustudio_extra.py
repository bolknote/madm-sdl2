#!/usr/bin/env python3
"""emuStudio SSEM examples and gobaby examples cross-check."""

from __future__ import annotations

import sys
from pathlib import Path

from convert_baby_source import parse_asm_text, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
EMU = SCRIPTS / "upstream" / "emustudio"
GOBABY = SCRIPTS / "upstream" / "gobaby-examples"
GOBABY_REPO = SCRIPTS / "upstream" / "gobaby" / "gobaby" / "examples"


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


def emit(name: str, title: str, url: str, asm: Path) -> None:
    words, ci = parse_asm_text(asm.read_text())
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def main() -> int:
    if (EMU / "ssem.ssem").is_file():
        emit(
            "emustudio_ssem_animation.store",
            "emuStudio — self-modifying “SSEM” CRT animation",
            "https://github.com/emustudio/emuStudio/blob/develop/plugins/compiler/as-ssem/src/main/examples/ssem.ssem",
            EMU / "ssem.ssem",
        )
    if (EMU / "add_5_3.ssem").is_file():
        emit(
            "emustudio_add_5_3.store",
            "emuStudio docs — addition 5 + 3 (result in line 9)",
            "https://www.emustudio.org/emustudio-documentation/as-ssem/",
            EMU / "add_5_3.ssem",
        )

    for asm_dir, prefix in ((GOBABY, "gobaby"), (GOBABY_REPO, "gobaby")):
        if not asm_dir.is_dir():
            continue
        for stem, out, blurb in (
            ("simple_calc", "gobaby_simple_calc", "5 − 3 → line 9"),
            ("factor", "gobaby_factor", "factor 2^18"),
            ("primegen", "gobaby_primegen", "chainable primes"),
        ):
            path = asm_dir / f"{stem}.asm"
            if not path.is_file():
                continue
            words, ci = parse_asm_text(path.read_text())
            dup = same_as_catalog(words)
            print(f"{prefix}_{stem}.asm", "dup" if dup else "new", dup or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
