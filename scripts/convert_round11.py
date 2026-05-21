#!/usr/bin/env python3
"""Layer-9: CCS progref1.html patterns + A1/A2 emulator mini-tests + Gunkies link map."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

from convert_baby_source import enc, parse_asm_text, to_signed32, write_store

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
REFERENCE = ROOT / "reference"
PROGRAMS = ROOT / "programs"
UP = SCRIPTS / "upstream"

CCS_PROGREF = UP / "ccs-progref" / "progref1.html"
GUNKIES = UP / "gunkies-links" / "Small-Scale_Experimental_Machine"

# --- CCS / Computer50 Appendix A2 (same text as ssemref.html) ---
A2_ADD_XY = """
; A2.1 — add x+y via SUB (x=5, y=3 → line 30)
3: LDN 28
4: SUB 29
5: STO 30
6: LDN 30
7: STO 30
28: NUM 5
29: NUM 3
30: NUM 0
"""

A2_SMALL_CONSTANT = """
; A2.2 — line 20 = 1 for SUB and JMP indirect (CI←1 → line 2)
1: LDN 30
2: STO 30
9: SUB 20
10: CMP
11: JMP 20
12: STP
20: NUM 1
30: NUM 7
"""

A2_IDX_MOD_RUN = """
; A2.3 — one-step instruction modification (SUB 19 → SUB 18 in line 6)
6: SUB 19
12: LDN 6
13: STO 0
14: LDN 0
15: SUB 18
16: STO 6
17: STP
18: NUM -1
19: NUM 0
"""

A2_COUNTING_RUN = """
; A2.4 — increment counter in line 6 address field (manual line numbers)
6: LDN 21
12: LDN 6
13: STO 0
14: LDN 0
15: SUB 20
16: STO 6
17: CMP
18: JMP 0
19: STP
20: NUM 1
21: NUM 0
"""

# --- A1 mini-tests (generated from progref, not external .snp) ---
TEST_LDN_STO_SUB = """
1: LDN 28
2: SUB 29
3: STO 30
4: LDN 30
5: STO 31
6: STP
28: NUM 4
29: NUM 2
30: NUM 0
31: NUM 0
"""

TEST_CMP_JMP = """
; A1.1 — SUB/CMP/JMP indirect; line 10 holds CI-1 for destination line 6
6: SUB 19
7: CMP
8: JMP 10
9: STP
10: NUM 5
19: NUM 1
28: NUM 3
"""

TEST_JRP = """
; A1.2 — relative jump: JRP 11 adds store[11] to CI
1: LDN 28
2: JRP 11
3: STP
4: LDN 28
5: STP
11: NUM 1
28: NUM 1
"""

TEST_FUNC5_SUB = """
1: SUB5 30
2: SUB 30
3: STP
30: NUM 3
"""

TEST_CI_WRAP = """
; A1.3 — CMP at line 30: negative acc → execute line 0
27: LDN 28
28: NUM 1
29: NUM 0
30: CMP
31: STP
0: LDN 28
1: STP
"""

TEST_INSN_AS_DATA = A2_IDX_MOD_RUN


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


def parse_progref_asm(text: str) -> tuple[list[int], int | None]:
    """Like parse_asm_text but accepts SUB5 for undocumented function 5 (=SUB)."""
    store = [0] * 32
    first_code_line: int | None = None
    for raw in text.strip().splitlines():
        line = raw.split("--")[0].split(";")[0].strip()
        if not line or re.fullmatch(r"\d+", line):
            continue
        m = re.match(r"^(\d+)\s*:?\s*(\w+)(?:\s+(.+))?$", line)
        if not m:
            continue
        addr = int(m.group(1))
        if addr >= 32:
            continue
        mnem = m.group(2).upper()
        rest = (m.group(3) or "").strip()
        arg = int(rest.split()[0]) if rest and re.match(r"-?\d+", rest.split()[0]) else 0
        if mnem == "SUB5":
            store[addr] = enc(5, arg)
            if first_code_line is None:
                first_code_line = addr
        elif mnem in ("NUM",):
            store[addr] = to_signed32(arg)
        else:
            from convert_baby_source import OP

            if mnem in OP:
                store[addr] = enc(OP[mnem], arg)
                if first_code_line is None:
                    first_code_line = addr
            elif mnem in ("BNUM", "BIN", "BINS"):
                from convert_baby_source import bnum_to_word

                store[addr] = bnum_to_word(rest.split()[0] if rest else "0")
            else:
                raise ValueError(f"unknown mnemonic {mnem!r}")
    if first_code_line is None:
        ci = None
    elif first_code_line == 0:
        ci = -1
    else:
        ci = first_code_line - 1
    return store, ci


def emit(name: str, title: str, url: str, text: str, *, use_sub5: bool = False) -> None:
    parser = parse_progref_asm if use_sub5 else parse_asm_text
    words, ci = parser(text)
    if not any(words):
        print("skip", name, "empty", file=sys.stderr)
        return
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def sync_ccs_refs() -> None:
    ref = REFERENCE / "ccs-progref"
    ref.mkdir(parents=True, exist_ok=True)
    if CCS_PROGREF.is_file():
        shutil.copy2(CCS_PROGREF, ref / "progref1.html")
    patterns = {
        "add_xy_pattern.asm": A2_ADD_XY,
        "small_constant_loop.asm": A2_SMALL_CONSTANT,
        "instruction_modification_pattern.asm": A2_IDX_MOD_RUN,
        "counting_in_instruction_pattern.asm": A2_COUNTING_RUN,
    }
    for fname, body in patterns.items():
        (ref / fname).write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote reference/ccs-progref/*.asm")


def sync_gunkies_map() -> None:
    dst = REFERENCE / "gunkies_baby_links.md"
    links = [
        ("Original paper (Williams & Kilburn)", "https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/kgill/mark1/ssem.html"),
        ("The Baby (new.baby.html)", "https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/new.baby.html"),
        ("Mark 1 Documents", "https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/kgill/mark1/mark1book.html"),
        ("Programmer's Reference (curation)", "https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/prog98/ssemref.html"),
        ("CCS progref1 (duplicate manual)", "https://www.cs.man.ac.uk/CCS/SSEM/progref1.html"),
        ("Kilburn memories (CCS)", "http://www.cs.man.ac.uk/CCS/res/res02.htm#e"),
        ("Rebuilding the Baby (Digital60)", "https://curation.cs.manchester.ac.uk/digital60/www.digital60.org/rebuild/"),
        ("CCS SSEM volunteers docs", "https://computerconservationsociety.org/ssemvolunteers/volunteers/"),
    ]
    lines = [
        "# Computer History Wiki — Manchester Baby external links",
        "",
        "Source: [gunkies.org/wiki/Manchester_Baby](https://gunkies.org/wiki/Manchester_Baby) "
        "(redirect from Small-Scale_Experimental_Machine).",
        "",
        "No program binaries on the wiki page; use as a link map to primary sources.",
        "",
        "| Resource | URL |",
        "|----------|-----|",
    ]
    for title, url in links:
        lines.append(f"| {title} | {url} |")
    if GUNKIES.is_file():
        lines.extend(["", f"Cached HTML: `scripts/upstream/gunkies-links/Small-Scale_Experimental_Machine`"])
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", dst.relative_to(ROOT))


def main() -> int:
    sync_ccs_refs()
    sync_gunkies_map()
    url = "https://www.cs.man.ac.uk/CCS/SSEM/progref1.html"
    emit(
        "ccs_progref_add_xy.store",
        "CCS progref A2.1 — add x+y via SUB",
        url + "#A2.1",
        A2_ADD_XY,
    )
    emit(
        "ccs_progref_small_constant_loop.store",
        "CCS progref A2.2 — decrement loop (dual-use line 20)",
        url + "#A2.2",
        A2_SMALL_CONSTANT,
    )
    emit(
        "ccs_progref_instruction_mod.store",
        "CCS progref A2.3 — instruction modification (one step)",
        url + "#A2.3",
        A2_IDX_MOD_RUN,
    )
    emit(
        "ccs_progref_counting.store",
        "CCS progref A2.4 — counter in instruction address field",
        url + "#A2.4",
        A2_COUNTING_RUN,
    )
    test_url = url + " Appendix 1"
    emit("progref_test_ldn_sto_sub.store", "progref test — LDN/SUB/STO add fragment", test_url, TEST_LDN_STO_SUB)
    emit("progref_test_cmp_jmp_indirect.store", "progref A1.1 — CMP + JMP indirect loop", test_url, TEST_CMP_JMP)
    emit("progref_test_jrp_relative.store", "progref A1.2 — JRP relative jump", test_url, TEST_JRP)
    emit(
        "progref_test_func5_alias_sub.store",
        "progref — function 5 same as SUB (MADM optab)",
        test_url,
        TEST_FUNC5_SUB,
        use_sub5=True,
    )
    emit("progref_test_ci_wraparound.store", "progref A1.3 — CMP at line 30 → line 0", test_url, TEST_CI_WRAP)
    emit(
        "progref_test_instruction_as_data.store",
        "progref A2.3 — instruction as data",
        test_url,
        TEST_INSN_AS_DATA,
    )
    print("Layer 9 done — see reference/LAYER9_HARVEST.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
