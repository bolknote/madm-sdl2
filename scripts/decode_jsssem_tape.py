#!/usr/bin/env python3
"""Decode JsSSEM base-32 paper tapes (from jsssem.html)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

TURING = '/E@A:SIU½DRJNFCKTZLWHYPQOBG"MXV£'
TN = {c: i for i, c in enumerate(TURING)}


def from_turing(word: str) -> int:
    n = 0
    for i, ch in enumerate(word[:7]):
        n += TN[ch] * (32**i)
    if n >= 2**31:
        n -= 2**32
    return n


def tape_to_store(tape: str) -> list[int]:
    t = tape.upper().replace(";", "½").replace("!", "£")
    word = ""
    store: list[int] = []
    for c in t:
        if c in " \n\r\t":
            continue
        word += c
        if len(word) == 7:
            store.append(from_turing(word))
            word = ""
    return store


def extract_tapes(html: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in re.finditer(r"var (\w+) = '([^']+)';", html):
        out[m.group(1)] = m.group(2)
    return out


def main() -> int:
    html = Path(__file__).parent / "upstream" / "jsssem.html"
    if not html.is_file():
        print("missing", html, file=sys.stderr)
        return 1
    tapes = extract_tapes(html.read_text())
    for name in ("fib", "prisoner", "addition", "multip", "wheeler"):
        if name not in tapes:
            continue
        store = tape_to_store(tapes[name])
        print(name, "len", len(store))
        for i, v in enumerate(store):
            print(f"  @{i} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
