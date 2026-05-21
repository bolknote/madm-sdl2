#!/usr/bin/env python3
"""Round-5 harvest: C88 VHDL test benches → ssem-inspired/c88/*.c88ram (not MADM .store)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
C88 = SCRIPTS / "upstream" / "ssem-inspired" / "c88" / "C88"
OUT = SCRIPTS.parent / "ssem-inspired" / "c88"

CELL_RE = re.compile(r'"([01]{8})"')


def parse_vhd_program(path: Path) -> list[str]:
    text = path.read_text()
    m = re.search(r"constant\s+test_program\s*:\s*cell_select_array\s*:=\s*\((.*?)\);", text, re.S)
    if not m:
        raise ValueError(f"no test_program in {path}")
    cells = CELL_RE.findall(m.group(1))
    if len(cells) != 8:
        raise ValueError(f"{path}: expected 8 cells, got {len(cells)}")
    return cells


def write_c88ram(path: Path, cells: list[str], source: str) -> None:
    lines = [
        f"; {source}",
        "; C88 homebrew: 8 addresses × 8 bits (VHDL std_logic_vector, MSB-left).",
        "; Not compatible with Manchester Baby 32×32 .store — see ssem-inspired/README.md",
        "",
    ]
    lines.extend(cells)
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    if not C88.is_dir():
        print(f"Missing {C88}; run download_upstream.sh first", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    tests = sorted(C88.glob("test_program_*.vhd"))
    if not tests:
        print("No test_program_*.vhd in C88 tree", file=sys.stderr)
        return 1

    for vhd in tests:
        stem = vhd.stem.replace("test_program_", "c88_test_")
        cells = parse_vhd_program(vhd)
        out = OUT / f"{stem}.c88ram"
        write_c88ram(out, cells, f"lexbailey/C88 {vhd.name}")
        print(f"wrote {out.relative_to(SCRIPTS.parent)}")

    print(f"done: {len(tests)} C88 RAM images under ssem-inspired/c88/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
