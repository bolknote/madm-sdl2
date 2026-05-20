#!/usr/bin/env python3
"""Build .store files from CCS diagnostic PDF text (pdftotext output)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import bits_to_word, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
PDF_TEXT = SCRIPTS / "upstream" / "ccs" / "diagnostic.txt"
PDF_URL = (
    "https://computerconservationsociety.org/ssemvolunteers/volunteers/"
    "Baby%20Functions%20Diagnostic%20Test%20Files%20-%20Analysis.1.0.pdf"
)

TESTS = [
    "JMP1Test",
    "JRP1Test",
    "LDN1Test",
    "STO1Test",
    "STO2Test",
    "SUB1Test",
    "CMP1Test",
    "CMP2Test",
    "ALL1Test",
]


LINE_RE = re.compile(r"^(\d{4}):\s*([01]{32})\s*$", re.MULTILINE)


def extract_dump(text: str, name: str) -> list[int] | None:
    """Find 32-line dump after 'Load {name}' in the PDF text."""
    needle = f"Load {name}"
    idx = text.find(needle)
    if idx < 0:
        needle = f"Load {name}."
        idx = text.find(needle)
    if idx < 0:
        return None
    chunk = text[idx : idx + 5000]
    lines = LINE_RE.findall(chunk)
    if len(lines) < 32:
        return None
    store = [0] * 32
    for addr_s, bits in lines[:32]:
        store[int(addr_s, 10)] = bits_to_word(bits)
    return store


def main() -> int:
    if not PDF_TEXT.is_file():
        print("missing", PDF_TEXT, "— run pdftotext on CCS PDF first", file=sys.stderr)
        return 1
    text = PDF_TEXT.read_text(encoding="utf-8", errors="replace")
    wrote = 0
    for name in TESTS:
        store = extract_dump(text, name)
        if store is None:
            print("skip (no dump)", name)
            continue
        out = PROGRAMS / f"ccs_{name.lower()}.store"
        write_store(
            out,
            f"CCS/MOSI diagnostic — {name}",
            PDF_URL,
            store,
            ci_start=-1,
        )
        print("wrote", out.name)
        wrote += 1
    return 0 if wrote else 1


if __name__ == "__main__":
    raise SystemExit(main())
