#!/usr/bin/env python3
"""
Regenerate davidsharp_*.store from David Sharp's online Baby program archive.

Fetches .asm / .snp over HTTP (nothing saved under programs/). Requires network.

https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program/
"""

from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

DAVIDSHARP_BASE = (
    "https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program"
)

DAVIDSHARP_PROGRAMS = [
    ("diffeqt.asm", "Parabola plot"),
    ("flash.asm", "Flashing / timing pattern"),
    ("hcf.asm", "Highest common factor"),
    ("hfr989.asm", "Highest factor routine variant"),
    ("intdiv.snp", "Integer division"),
    ("longdiv2.snp", "Long division"),
    ("medclock.snp", "Medieval analog clock"),
    ("nightmare.snp", "Tom Kilburn's Nightmare"),
    ("noodletimer.snp", "3-minute noodle timer"),
    ("primegen.asm", "Prime generator"),
    ("slide9.snp", "Sliding display"),
    ("virpet.asm", "Virtual pet"),
]

OP = {
    "JMP": 0,
    "JRP": 1,
    "JMR": 1,
    "JPR": 1,
    "LDN": 2,
    "STO": 3,
    "SUB": 4,
    "CMP": 6,
    "SKN": 6,
    "STP": 7,
    "STOP": 7,
    "HLT": 7,
}


def enc(op: int, addr: int) -> int:
    return (op << 13) | (addr & 31)


def to_signed32(v: int) -> int:
    v &= 0xFFFFFFFF
    return v - 0x100000000 if v >= 0x80000000 else v


def bits_to_word(bits: str) -> int:
    bits = bits.strip()
    if len(bits) != 32:
        raise ValueError(f"expected 32 bits, got {len(bits)}: {bits!r}")
    return to_signed32(sum(int(bits[i]) << i for i in range(32)))


def write_store(
    path: Path,
    title: str,
    source_url: str,
    words: list[int],
    *,
    ci_start: int | None = None,
) -> None:
    lines = [f"# {title}", f"# {source_url}", "#"]
    if ci_start is not None:
        lines.append(f"# ci-start {ci_start}")
    for i, w in enumerate(words[:32]):
        if w == 0:
            lines.append(f"@{i} 0")
        elif 0 < w < 0x10000:
            lines.append(f"@{i} {w}")
        elif w > 0:
            lines.append(f"@{i} 0x{w:x}")
        else:
            lines.append(f"@{i} {w}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def bnum_to_word(bits: str) -> int:
    """NevynUK BNUM/BIN: expand a short bit pattern into 32 store bits."""
    value = int(bits, 2)
    store = 0
    for _ in range(32):
        store = (store << 1) & 0xFFFFFFFF
        if value & 1:
            store |= 1
        value >>= 1
    return to_signed32(store)


def parse_asm_text(text: str) -> tuple[list[int], int | None]:
    store = [0] * 32
    first_code_line: int | None = None
    for raw in text.strip().splitlines():
        line = raw.split("--")[0].strip()
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
        if mnem in ("BNUM", "BIN", "BINS"):
            store[addr] = bnum_to_word(rest.split()[0] if rest else "0")
            continue
        arg = int(rest.split()[0]) if rest and re.match(r"-?\d+", rest.split()[0]) else 0
        if mnem == "NUM":
            store[addr] = to_signed32(arg)
        elif mnem in OP:
            store[addr] = enc(OP[mnem], arg)
            if first_code_line is None and mnem not in ("CMP", "SKN", "STP", "STOP", "HLT"):
                first_code_line = addr
            elif first_code_line is None and mnem in ("CMP", "SKN", "STP", "STOP", "HLT"):
                first_code_line = addr
        else:
            raise ValueError(f"unknown mnemonic {mnem!r} in {raw!r}")
    if first_code_line is None:
        ci = None
    elif first_code_line == 0:
        ci = -1
    else:
        ci = first_code_line - 1
    return store, ci


def _parse_operand(token: str, labels: dict[str, int]) -> int:
    token = token.strip()
    if not token:
        return 0
    if token in labels:
        return labels[token]
    if re.match(r"-?0x[0-9a-fA-F]+$", token):
        return int(token, 0)
    if re.match(r"-?\d+$", token):
        return int(token, 10)
    raise ValueError(f"unknown operand {token!r}")


def parse_babyutils_asm(text: str) -> tuple[list[int], int | None]:
    """Andy Bower babyutils: labels, EJA, implicit line addresses."""
    records: list[tuple[int | None, str | None, str]] = []
    for raw in text.strip().splitlines():
        line = raw.split("--")[0].strip()
        if not line:
            continue
        m = re.match(r"^(\d+)\s*:\s*(.*)$", line)
        if m:
            org = int(m.group(1))
            rest = m.group(2).strip()
            records.append((org, None, rest))
            continue
        m = re.match(r"^(\w+)\s*:\s*(.*)$", line)
        if m and m.group(1).upper() not in OP and m.group(1).upper() not in (
            "NUM",
            "EJA",
            "BNUM",
            "BIN",
            "HLT",
        ):
            records.append((None, m.group(1), m.group(2).strip()))
            continue
        records.append((None, None, line))

    labels: dict[str, int] = {}
    cursor = 0
    pending_label: str | None = None
    layout: list[tuple[int, str, str]] = []

    for org, label, body in records:
        if org is not None:
            cursor = org
        if label:
            labels[label] = cursor
        if not body:
            continue
        parts = body.split(None, 2)
        mnem = parts[0].upper()
        rest = parts[1] if len(parts) > 1 else ""
        layout.append((cursor, mnem, rest))
        cursor += 1

    store = [0] * 32
    first_code: int | None = None
    for addr, mnem, rest in layout:
        if addr >= 32:
            raise ValueError(f"address {addr} >= 32")
        if mnem == "NUM":
            store[addr] = to_signed32(_parse_operand(rest.split()[0], labels))
        elif mnem == "EJA":
            store[addr] = to_signed32(_parse_operand(rest.split()[0], labels) - 1)
        elif mnem in OP:
            op = OP[mnem]
            arg = _parse_operand(rest.split()[0], labels) if rest else 0
            store[addr] = enc(op, arg)
            if first_code is None:
                first_code = addr
        else:
            raise ValueError(f"unknown mnemonic {mnem!r}")
    if first_code is None:
        ci = None
    elif first_code == 0:
        ci = -1
    else:
        ci = first_code - 1
    return store, ci


def parse_snp_text(text: str) -> tuple[list[int], int | None]:
    store = [0] * 32
    first_line: int | None = None
    for raw in text.strip().splitlines():
        line = raw.strip()
        if not line or re.fullmatch(r"\d+", line):
            continue
        m = re.match(r"^(\d{1,4}):([01]{32})$", line)
        if not m:
            continue
        addr = int(m.group(1))
        if addr >= 32:
            continue
        store[addr] = bits_to_word(m.group(2))
        if first_line is None:
            first_line = addr
    ci = -1 if first_line == 0 else None
    return store, ci


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read().decode("utf-8", errors="replace")


def convert_url(url: str, name: str) -> tuple[list[int], int | None]:
    text = fetch_text(url)
    if name.endswith(".asm"):
        return parse_asm_text(text)
    if name.endswith(".snp"):
        return parse_snp_text(text)
    raise ValueError(name)


def main() -> int:
    root = Path(__file__).resolve().parent.parent / "programs"
    for name, description in DAVIDSHARP_PROGRAMS:
        url = f"{DAVIDSHARP_BASE}/{name}"
        store, ci = convert_url(url, name)
        dst = root / f"davidsharp_{Path(name).stem}.store"
        write_store(
            dst,
            f"David Sharp — {description}",
            url,
            store,
            ci_start=ci,
        )
        print("wrote", dst.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
