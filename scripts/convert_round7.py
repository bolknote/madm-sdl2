#!/usr/bin/env python3
"""Round-7: emuStudio as-ssem examples, Cambridge SVBaby map, upstream harvest notes."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import bits_to_word, parse_asm_text, write_store

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
PROGRAMS = ROOT / "programs"
EMU = SCRIPTS / "upstream" / "emustudio-full" / "emuStudio" / "plugins" / "compiler" / "as-ssem" / "src" / "main" / "examples"
EMU_URL = "https://github.com/emustudio/emuStudio/tree/develop/plugins/compiler/as-ssem/src/main/examples"
CAM = SCRIPTS / "upstream" / "cambridge-deep"


def preprocess_ssem(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.split("--")[0].split(";")[0].strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


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


def emit(stem: str, title: str, asm: Path) -> None:
    out = PROGRAMS / f"emustudio_{stem}.store"
    words, ci = parse_asm_text(preprocess_ssem(asm.read_text()))
    dup = same_as_catalog(words)
    if dup:
        print("skip", out.name, f"dup {dup}", file=sys.stderr)
        return
    write_store(out, title, f"{EMU_URL}/{asm.name}", words, ci_start=ci)
    print("wrote", out.name)


def parse_prog_sv(path: Path) -> list[int]:
    return [bits_to_word(m.group(1)) for m in re.finditer(r"32'b([01]{32})", path.read_text())]


def document_cambridge_sv() -> None:
    ref = ROOT / "reference" / "cambridge_svbaby_switch_map.md"
    ref.parent.mkdir(parents=True, exist_ok=True)
    ref.write_text(
        """# Cambridge SVBaby switch map (Richard Leivers, 2009)

Source: `scripts/upstream/cambridge-deep/SVBaby/baby.sv`

| Switch | Module | SNP source | Catalog equivalent |
|--------|--------|------------|-------------------|
| SW15 (default) | `progNIGHT` → prog1 | `NIGHT.SNP` | `davidsharp_nightmare` / `nevynuk_nightmare` |
| SW16 | `progNOODLE` → prog2 | `NOODLE.SNP` | `davidsharp_noodletimer` / `nevynuk_3minutes` |
| SW17 | `progFIB` → prog3 | `FIB.SNP` | `cambridge_fib` |

`progPARABOLA.sv` exists but is **not** wired to switches (only three programs instantiated).

JavaBaby.zip / BabySNPtoV.zip also ship: `FACTOR`, `DIVIDE`, `CLOCK`, `PARABOLA` — all byte-identical to existing catalog entries.
"""
    )
    print("wrote", ref.relative_to(ROOT))


def main() -> int:
    if not EMU.is_dir():
        print("missing", EMU, "— clone emuStudio as-ssem (download_upstream.sh)", file=sys.stderr)
        return 1

    meta = {
        "addition": "Addition 5 + 3 (operands in lines 29–30)",
        "bcs-division": "BCS division example",
        "dec-till-negative": "Decrement until accumulator negative",
        "highest-common-factor": "Highest common factor",
        "highest-factor": "Highest proper factor (emuStudio layout)",
        "medclock": "Medclock display",
        "nightmare": "Nightmare animation",
        "noodle-timer": "Noodle timer",
        "square-root": "Square root",
        "the-fraj": "The Fraj",
    }
    skip = {"ssem", "virpet", "primegen", "parabola"}
    for stem, blurb in meta.items():
        asm = EMU / f"{stem}.ssem"
        if not asm.is_file() or stem in skip:
            continue
        emit(stem.replace("-", "_"), f"emuStudio — {blurb}", asm)

    if CAM.is_dir():
        document_cambridge_sv()
        for label, sv, snp in (
            ("prog1_night", "progNIGHT.sv", "NIGHT"),
            ("prog2_noodle", "progNOODLE.sv", "NOODLE"),
            ("prog3_fib", "progFIB.sv", "FIB"),
        ):
            path = CAM / "SVBaby" / sv
            if path.is_file():
                words = parse_prog_sv(path)
                dup = same_as_catalog(words)
                print(f"cambridge {label}: dup {dup}" if dup else f"cambridge {label}: NEW")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
