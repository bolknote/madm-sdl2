#!/usr/bin/env python3
"""Fox book machine-code dump, Retro SE factor.asm, comparch Logisim RAM."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from convert_baby_source import bits_to_word, parse_asm_text, to_signed32, write_store

SCRIPTS = Path(__file__).resolve().parent
PROGRAMS = SCRIPTS.parent / "programs"
UP = SCRIPTS / "upstream"

FOX_HTML = UP / "fox-book" / "fox.html"
FOX_BITS = UP / "fox-book" / "TuringLongDivision.machine.txt"
LOGISIM = UP / "comparch" / "comparch" / "chapter07" / "TuringLongDivision.logisimRAMImage"
RETRO_ASM = UP / "retro-factor" / "factor.asm"
GOBABY_ASM = UP / "gobaby" / "gobaby" / "examples" / "factor.asm"


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


def fox_words_from_html() -> list[int]:
    if not FOX_HTML.is_file():
        raise FileNotFoundError(FOX_HTML)
    text = FOX_HTML.read_text()
    idx = text.lower().find("machine code for turing")
    if idx < 0:
        raise ValueError("phrase 'machine code for Turing' not found in fox.html")
    snippet = text[idx : idx + 12000]
    bits = re.findall(r"[01]{32}", snippet)
    if len(bits) < 32:
        raise ValueError(f"expected 32 bit lines, got {len(bits)}")
    FOX_BITS.write_text("\n".join(bits[:32]) + "\n")
    return [bits_to_word(b) for b in bits[:32]]


def logisim_words() -> list[int]:
    lines = [
        ln.strip()
        for ln in LOGISIM.read_text().splitlines()
        if re.fullmatch(r"[0-9a-fA-F]+", ln.strip())
    ]
    return [to_signed32(int(x, 16)) for x in lines[:32]]


def emit(name: str, title: str, url: str, words: list[int], ci: int | None = -1) -> None:
    dup = same_as_catalog(words)
    if dup:
        print("skip", name, f"dup {dup}", file=sys.stderr)
        return
    write_store(PROGRAMS / name, title, url, words, ci_start=ci)
    print("wrote", name)


def main() -> int:
    if FOX_HTML.is_file():
        fw = fox_words_from_html()
        if LOGISIM.is_file():
            lw = logisim_words()
            if fw != lw:
                print("warn: fox.html bits != Logisim RAM", file=sys.stderr)
        emit(
            "fox_book_turing_longdiv.store",
            "Charles Fox book — Turing long division machine code (32 LSB-left lines)",
            "https://dokumen.pub/computer-architecture-from-the-stone-age-to-the-quantum-age-9781718502864-9781718502871.html",
            fw,
            -1,
        )

    for asm_path, stem, url in (
        (
            RETRO_ASM,
            "retro_factor",
            "https://retrocomputing.stackexchange.com/a/2869",
        ),
        (
            GOBABY_ASM,
            "gobaby_factor_retro",
            "https://github.com/jcla1/gobaby/blob/main/examples/factor.asm",
        ),
    ):
        if not asm_path.is_file():
            print("skip", asm_path, "missing", file=sys.stderr)
            continue
        words, ci = parse_asm_text(asm_path.read_text())
        emit(
            f"{stem}.store",
            f"First Baby factor program (2^18) — {asm_path.name}",
            url,
            words,
            ci,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
