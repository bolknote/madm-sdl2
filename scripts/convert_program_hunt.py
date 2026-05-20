#!/usr/bin/env python3
"""Build .store files from program-hunt sources (HASE, JsSSEM, Rosetta, CCS guide)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import (
    OP,
    bits_to_word,
    enc,
    parse_asm_text,
    parse_snp_text,
    to_signed32,
    write_store,
)

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
UP = SCRIPTS / "upstream"

HASE_DIR = UP / "hase" / "mu_baby-4.1"
GUIDE_TXT = UP / "hase" / "guide.txt"

JSSSEM_HTML = UP / "jsssem.html"
TURING_ALPHABET = '/E@A:SIU½DRJNFCKTZLWHYPQOBG"MXV£'
TURING_MAP = {c: i for i, c in enumerate(TURING_ALPHABET)}

ROSETTA_STOP = "00000000000001110000000000000000"
ROSETTA_EMPTY = "00000000000000000000000000000000"
ROSETTA_HELLO = """
01100000000001110000000000000000
10000000000001010000000000000000
10011101110111011101010111000000
10010101010101010101010101000000
10010101010101010101010111000000
10011101110111011100110100000010
10000000000000000000010011000010
10011000000000000000100000000100
01101000000000000001000000000000
00000000000000000000000000000000
00000000000000000000000000000000
00100100100000000010000100100000
00100100100000000010000100100000
00100100101110111010011100100000
00100100101010100010010100100000
00100100101010100010010100000000
00100100101110100011011100100000
00011011000000000000000000000000
""".strip()


def hase_programs() -> list[tuple[str, str, str, list[str], list[str]]]:
    prog_path = HASE_DIR / "INPUT.prog_mem.mem"
    data_path = HASE_DIR / "INPUT.data_mem.mem"
    if not prog_path.is_file():
        raise FileNotFoundError(prog_path)
    prog_lines = prog_path.read_text().splitlines()
    data_lines = data_path.read_text().splitlines()
    blocks: list[tuple[list[str], list[str]]] = []
    cur_p: list[str] = []
    cur_d: list[str] = []
    for p, d in zip(prog_lines, data_lines):
        if p.strip() == "EOP":
            if cur_p:
                blocks.append((cur_p, cur_d))
            cur_p, cur_d = [], []
        else:
            cur_p.append(p.strip())
            cur_d.append(d.strip())
    meta = [
        (
            "hase_insn_demo.store",
            "HASE mu_baby — all SSEM instructions demo",
            "https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/ssem/mu_baby_v4.1.zip",
        ),
        (
            "hase_highest_factor.store",
            "HASE mu_baby — highest factor (18 July 1948 program)",
            "https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/ssem/mu_baby_v4.1.zip",
        ),
        (
            "hase_third_demo.store",
            "HASE mu_baby — third built-in demo (CRT pattern)",
            "https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/ssem/mu_baby_v4.1.zip",
        ),
    ]
    return [(meta[i][0], meta[i][1], meta[i][2], p, d) for i, (p, d) in enumerate(blocks)]


def hase_to_store(prog_lines: list[str], data_lines: list[str]) -> list[int]:
    """Map HASE INPUT loader: insn at store line i+1; data after last insn line."""
    store = [0] * 32
    for i, ins in enumerate(prog_lines):
        m = re.match(r"^(\w+)\s+(-?\d+)$", ins.strip())
        if not m:
            continue
        mn, arg = m.group(1), int(m.group(2))
        if mn in OP:
            line = i + 1
            if line < 32:
                store[line] = enc(OP[mn], arg)
    last_inst_line = len(prog_lines) + 1
    for j, raw in enumerate(data_lines):
        addr = last_inst_line + j
        if addr >= 32:
            break
        store[addr] = to_signed32(int(raw))
    return store


def guide_factorct() -> tuple[list[int], int | None]:
    if not GUIDE_TXT.is_file():
        raise FileNotFoundError(GUIDE_TXT)
    text = GUIDE_TXT.read_text()
    lines: list[tuple[int, str]] = []
    for raw in text.splitlines():
        m = re.match(r"^(\d{4}):\s*([01]{32})$", raw.strip())
        if m:
            lines.append((int(m.group(1)), m.group(2)))
    # First contiguous 0000:..0031: block under "Program Code"
    start = None
    for i, (addr, _) in enumerate(lines):
        if addr == 0 and start is None:
            start = i
        elif start is not None and addr == 0 and i > start:
            break
    if start is None:
        raise ValueError("no Program Code dump in guide.txt")
    chunk = "\n".join(f"{a:04d}:{b}" for a, b in lines[start : start + 32])
    return parse_snp_text(chunk)


def from_turing_word(word: str) -> int:
    n = 0
    for i, ch in enumerate(word[:7]):
        n += TURING_MAP[ch] * (32**i)
    if n >= 2**31:
        n -= 2**32
    return n


def jsssem_tape_to_store(tape: str) -> list[int]:
    t = tape.upper().replace(";", "½").replace("!", "£")
    word = ""
    store: list[int] = []
    for c in t:
        if c in " \n\r\t":
            continue
        word += c
        if len(word) == 7:
            store.append(from_turing_word(word))
            word = ""
    while len(store) < 32:
        store.append(0)
    return store[:32]


def jsssem_tapes_from_html(html: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in re.finditer(r"var (\w+) = '([^']+)';", html)}


def bits_lines_to_store(text: str) -> list[int]:
    store = [0] * 32
    for i, line in enumerate(text.strip().splitlines()):
        bits = line.strip()
        if len(bits) == 32 and set(bits) <= {"0", "1"}:
            store[i] = bits_to_word(bits)
    return store


def main() -> int:
    if not HASE_DIR.is_dir():
        print("missing", HASE_DIR, "— unzip mu_baby_v4.1.zip under scripts/upstream/hase/", file=sys.stderr)
        return 1

    for fname, title, url, prog, data in hase_programs():
        store = hase_to_store(prog, data)
        write_store(PROGRAMS / fname, title, url, store, ci_start=-1)
        print("wrote", fname)

    jsssem_url = "http://www.edmundgriffiths.com/jsssem.html"
    if JSSSEM_HTML.is_file():
        tapes = jsssem_tapes_from_html(JSSSEM_HTML.read_text())
        jsssem_programs = [
            ("jsssem_fibo40.store", "JsSSEM — Fibonacci (40th term → A = 102334155)", "fib"),
            (
                "jsssem_prisoner.store",
                "JsSSEM — iterated Prisoner’s Dilemma vs Tit-for-Tat",
                "prisoner",
            ),
            ("jsssem_addition.store", "JsSSEM — add store(5) + store(6)", "addition"),
            ("jsssem_multiply.store", "JsSSEM — multiply store(29) × store(30)", "multip"),
            ("jsssem_wheeler.store", "JsSSEM — Wheeler jump / subroutine demo", "wheeler"),
        ]
        for fname, title, key in jsssem_programs:
            if key not in tapes:
                print("skip", fname, "— no tape", key, file=sys.stderr)
                continue
            store = jsssem_tape_to_store(tapes[key])
            write_store(PROGRAMS / fname, title, jsssem_url, store, ci_start=-1)
            print("wrote", fname)
    else:
        print("skip JsSSEM tapes — missing", JSSSEM_HTML, file=sys.stderr)

    write_store(
        PROGRAMS / "rosetta_stop.store",
        "Rosetta Code — minimal terminating SSEM program (STOP at line 0)",
        "https://rosettacode.org/wiki/Empty_program#SSEM",
        bits_lines_to_store(ROSETTA_STOP),
        ci_start=-1,
    )
    print("wrote rosetta_stop.store")

    write_store(
        PROGRAMS / "rosetta_empty_loop.store",
        "Rosetta Code — empty store (JMP 0 infinite loop)",
        "https://rosettacode.org/wiki/Empty_program#SSEM",
        [0] * 32,
        ci_start=-1,
    )
    print("wrote rosetta_empty_loop.store")

    hello = bits_lines_to_store(ROSETTA_HELLO)
    write_store(
        PROGRAMS / "rosetta_hello_graphical.store",
        "Rosetta Code — graphical Hello on Williams tube (STOP in line 0 bits)",
        "https://rosettacode.org/wiki/Hello_world/Graphical#SSEM",
        hello,
        ci_start=-1,
    )
    print("wrote rosetta_hello_graphical.store")

    if GUIDE_TXT.is_file():
        store, ci = guide_factorct()
        write_store(
            PROGRAMS / "ccs_factorct.store",
            "CCS guide — FACTORCT.SNP program code (full factor run layout)",
            "https://computerconservationsociety.org/ssemvolunteers/volunteers/A%20Technical%20Introduction%20To%20Programming%20the%20Baby%20v4.0.pdf",
            store,
            ci_start=ci,
        )
        print("wrote ccs_factorct.store")
    else:
        print("skip ccs_factorct — missing", GUIDE_TXT, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
