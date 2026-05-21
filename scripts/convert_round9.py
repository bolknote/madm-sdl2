#!/usr/bin/env python3
"""Layer-7 harvest: mirror babyutils/Fox/retro sources; no new unique .store images."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from convert_baby_source import parse_babyutils_asm

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
REFERENCE = ROOT / "reference"
PROGRAMS = ROOT / "programs"
UP = SCRIPTS / "upstream"

BABYUTILS_TEST = UP / "babyutils" / "babyutils" / "test"
COMPARCH_ASM = UP / "comparch" / "comparch" / "chapter07" / "TuringLongDivision.asm"
RETRO_HTML = UP / "retro-factor" / "factor.html"
NEVYN_CPP_TESTS = (
    UP / "nevynuk" / "ManchesterBaby" / "Source" / "CPP" / "NuttX" / "UnitTests"
)


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


def sync_babyutils_refs() -> list[str]:
    out_dir = REFERENCE / "babyutils"
    out_dir.mkdir(parents=True, exist_ok=True)
    notes: list[str] = []
    if not BABYUTILS_TEST.is_dir():
        print("warn: missing", BABYUTILS_TEST, file=sys.stderr)
        return notes
    for src in sorted(BABYUTILS_TEST.glob("*.asm")):
        dst = out_dir / src.name
        shutil.copy2(src, dst)
        notes.append(src.name)
        try:
            words, _ci = parse_babyutils_asm(src.read_text())
            dup = same_as_catalog(words)
            if dup:
                print("babyutils", src.name, "-> dup", dup)
            else:
                print("babyutils", src.name, "-> parseable, not in catalog")
        except Exception as exc:
            print("babyutils", src.name, "-> needs bas/macro expand:", exc)
    return notes


def sync_fox_ref() -> None:
    dst = REFERENCE / "fox_turing_long_division.asm"
    if COMPARCH_ASM.is_file():
        shutil.copy2(COMPARCH_ASM, dst)
        print("wrote", dst.relative_to(ROOT))
        return
    print("warn: missing", COMPARCH_ASM, file=sys.stderr)


def enrich_retro_factor() -> None:
    dst = REFERENCE / "retro_factor_gobaby.asm"
    if not RETRO_HTML.is_file():
        print("warn: missing", RETRO_HTML, file=sys.stderr)
        return
    text = RETRO_HTML.read_text()
    start = text.find("<pre><code>; This is the original factor")
    if start < 0:
        print("warn: retro factor <pre> block not found", file=sys.stderr)
        return
    end = text.find("</code></pre>", start)
    block = text[start:end]
    lines: list[str] = []
    for raw in block.splitlines():
        if raw.startswith("<pre><code>"):
            raw = raw[len("<pre><code>") :]
        if raw.startswith(";") or raw.strip():
            lines.append(raw.rstrip())
    body = "\n".join(lines).strip() + "\n"
    header = (
        "; Retrocomputing SE answer — Joseph Adams / gobaby factor 2^18\n"
        "; https://retrocomputing.stackexchange.com/a/2869\n"
        "; Run with: gobaby -t -l 27 -p=f examples/factor.asm\n"
        "; Catalog: programs/gobaby_factor.store (= ccs_factorct bytes)\n"
        ";\n"
    )
    dst.write_text(header + body)
    print("wrote", dst.relative_to(ROOT), f"({len(lines)} lines from HTML)")


def write_nevyn_cpp_note() -> None:
    dst = REFERENCE / "nevynuk_cpp_unit_tests.md"
    compiler = NEVYN_CPP_TESTS / "test_compiler.cxx"
    if not compiler.is_file():
        print("warn: missing", compiler, file=sys.stderr)
        return
    dst.write_text(
        """# NevynUK C++ unit tests (Mark Stevens port)

Path in upstream cache: `scripts/upstream/nevynuk/ManchesterBaby/Source/CPP/NuttX/UnitTests/`.

These tests exercise the **assembler/compiler API**, not separate runnable Baby demos:

| File | Role |
|------|------|
| `test_compiler.cxx` | `goodApplication[]` is a **partial** `hfr989.ssem` fragment (lines 01–08, 16–20) for lexer/parser tests |
| `test_storelines.cxx` | Store-line encoding API |
| `test_filesystem.cxx` | Loads `hfr989.ssem` and compares output to expected trace lines |
| `test_machine.cxx` / `test_program.cxx` | Machine/program objects |

Full program images remain under `SSEMPrograms/` and `SSEMApps/` (catalog: `nevynuk_*.store`).

No additional `.store` files were added from this tree in layer 7.
"""
    )
    print("wrote", dst.relative_to(ROOT))


def main() -> int:
    sync_babyutils_refs()
    sync_fox_ref()
    enrich_retro_factor()
    write_nevyn_cpp_note()
    print("Layer 7: reference sync only (see reference/LAYER7_HARVEST.md)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
