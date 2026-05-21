#!/usr/bin/env python3
"""Layer-6 harvest: Cambridge SVBaby prog1–3, upstream manifests, alias stores (optional)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

from convert_baby_source import bits_to_word, parse_asm_text, parse_snp_text, write_store

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
PROGRAMS = ROOT / "programs"
REF = ROOT / "reference"
UP = SCRIPTS / "upstream"
CAM = UP / "cambridge-deep"
SV = CAM / "SVBaby"
JAVA_ZIP = CAM / "JavaBaby.zip"
REPO_SV = "https://www.cl.cam.ac.uk/teaching/0910/ECAD%2BArch/files/SVBaby.zip"

SV_MAP = [
    ("prog1", "progNIGHT.sv", "NIGHT.SNP", "cambridge_sv_prog1_night"),
    ("prog2", "progNOODLE.sv", "NOODLE.SNP", "cambridge_sv_prog2_noodle"),
    ("prog3", "progFIB.sv", "FIB.SNP", "cambridge_sv_prog3_fib"),
]


def parse_prog_sv(path: Path) -> list[int]:
    return [bits_to_word(m.group(1)) for m in re.finditer(r"32'b([01]{32})", path.read_text())]


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


def words_to_snp_listing(words: list[int]) -> str:
    """Minimal SNP-style lines for reference (not full SNP format)."""
    lines = []
    for i, w in enumerate(words):
        if w == 0 and i > 20:
            continue
        lines.append(f"{i:02d}  word {w}")
    return "\n".join(lines) + "\n"


def export_cambridge_reference() -> None:
    REF.mkdir(parents=True, exist_ok=True)
    if JAVA_ZIP.is_file():
        for _, _, snp, _ in SV_MAP:
            try:
                data = subprocess.check_output(["unzip", "-p", str(JAVA_ZIP), snp]).decode()
                (REF / f"cambridge_{snp.replace('.SNP', '').lower()}.snp").write_text(data)
            except subprocess.CalledProcessError:
                pass

    for prog, sv_file, snp, ref_stem in SV_MAP:
        sv_path = SV / sv_file
        if not sv_path.is_file():
            print("missing", sv_path, file=sys.stderr)
            continue
        words = parse_prog_sv(sv_path)
        (REF / f"{ref_stem}.words.txt").write_text(words_to_snp_listing(words))
        dup = same_as_catalog(words)
        print(f"{prog}: SVBaby/{sv_file} -> dup {dup}" if dup else f"{prog}: NEW bytes")

    map_path = REF / "cambridge_svbaby_switch_map.md"
    if not map_path.is_file():
        print("note: run convert_round7.py for switch_map.md", file=sys.stderr)


def emit_alias_stores() -> None:
    """Pedagogical aliases (same bytes, explicit Cambridge SW15–17 names)."""
    titles = {
        "cambridge_sv_prog1_night": "Cambridge SVBaby SW15 — progNIGHT (prog1)",
        "cambridge_sv_prog2_noodle": "Cambridge SVBaby SW16 — progNOODLE (prog2)",
        "cambridge_sv_prog3_fib": "Cambridge SVBaby SW17 — progFIB (prog3)",
    }
    for prog, sv_file, _, out_stem in SV_MAP:
        words = parse_prog_sv(SV / sv_file)
        dup = same_as_catalog(words)
        out = PROGRAMS / f"{out_stem}.store"
        if dup and dup == out.name:
            print("skip", out.name, "already catalogued")
            continue
        if dup:
            print("skip", out.name, f"dup {dup} (use reference/{out_stem}.words.txt)", file=sys.stderr)
            continue
        write_store(out, titles[out_stem], f"{REPO_SV} — {sv_file}", words, ci_start=-1)
        print("wrote", out.name)


def copy_pico_program_c() -> None:
    src = UP / "pico-baby-if" / "pico-baby-if" / "program.c"
    if src.is_file():
        shutil.copy2(src, REF / "pico_baby_if_program.c")
        print("reference/pico_baby_if_program.c")


def write_layer6_report() -> None:
    report = REF / "LAYER6_HARVEST.md"
    report.write_text(
        """# Layer-6 harvest report

## Cambridge SVBaby (SW15–17)

| Switch | Module | SNP | Catalog duplicate |
|--------|--------|-----|-------------------|
| SW15 | progNIGHT | NIGHT.SNP | `davidsharp_nightmare`, `nevynuk_nightmare`, `babyping_kilburn` |
| SW16 | progNOODLE | NOODLE.SNP | `davidsharp_noodletimer`, `nevynuk_3minutes`, `babyping_noodle` |
| SW17 | progFIB | FIB.SNP | `cambridge_fib` |

`progPARABOLA.sv` exists but is **not** wired to switches.

Reference copies: `cambridge_*.snp`, `cambridge_sv_prog*.words.txt`.

## baby-emulator 0.2.1

- `new_example_program()` → `baby_rust_add5.store`
- README countdown ASM → `baby_rust_countdown.store`
- Unit tests: opcode/API tests only, **no** additional full 32-word programs

## NevynUK ManchesterBaby

- `SSEMApps/` = `SSEMPrograms/` (same `.ssem` set) → all `nevynuk_*.store`
- `Add.ssem` (10+5→15), `hfr989.ssem` in `reference/mark_stevens_*.ssem`

## SIMH

- `SSEM/` supports `.st` LOAD/DUMP; **no** sample `.st` files in tree

## JsSSEM / EMF

- JsSSEM: 5 tapes in catalog (`jsssem_*.store`)
- EMF: UI buttons reference David Sharp family; `.bys` not on server

## Pico / comparch / babyutils

- `pico-baby-if/program.c` = `nevynuk_turing_longdiv` (quotient @28 = 0)
- `comparch/chapter07/TuringLongDivision.asm` — same family
- babyutils `test/*.asm`: 4 in catalog; `ldiv*` = Turing dup; `macro`/`madd2`/EJA need expand

## gobaby

Only `examples/{factor,primegen,simple_calc}.asm` — all in catalog.

## emuStudio

See `convert_round7.py` — 10 unique `emustudio_*.store` added.
"""
    )
    print("wrote reference/LAYER6_HARVEST.md")


def main() -> int:
    if not SV.is_dir():
        print("missing", SV, "— run download_upstream.sh", file=sys.stderr)
        return 1
    export_cambridge_reference()
    copy_pico_program_c()
    write_layer6_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
