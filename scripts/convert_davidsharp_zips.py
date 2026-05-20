#!/usr/bin/env python3
"""Build .store files from David Sharp ssem.jar / baby.zip extras (e.g. Baby9.snp)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from convert_baby_source import parse_snp_text, write_store

PROGRAMS = Path(__file__).resolve().parent.parent / "programs"
SCRIPTS = Path(__file__).resolve().parent
DS = SCRIPTS / "upstream" / "davidsharp_zips"
JAR = DS / "unpacked" / "ssem" / "ssem.jar"
BABY9_SNPS = [
    (JAR, "Baby9.snp"),
    (DS / "unpacked" / "src" / "src" / "Baby9.snp", None),
]


def snp_bytes(path: Path, inner: str | None) -> str:
    if inner:
        return subprocess.check_output(["unzip", "-p", str(path), inner]).decode()
    return path.read_text(encoding="utf-8")


def main() -> int:
    if not JAR.is_file():
        print("missing", JAR, "— unpack davidsharp_zips first", file=sys.stderr)
        return 1

    src = DS / "unpacked" / "src" / "src" / "Baby9.snp"
    data = snp_bytes(JAR, "Baby9.snp")
    store, ci = parse_snp_text(data)
    write_store(
        PROGRAMS / "davidsharp_baby9.store",
        "Baby9 marquee (Keith Wood; ssem.jar 2008, differs from slide9.snp)",
        "https://www.davidsharp.com/baby/ssem.zip",
        store,
        ci_start=ci,
    )
    print("wrote davidsharp_baby9.store", "ci", ci)
    if src.is_file():
        s2, _ = parse_snp_text(src.read_text(encoding="utf-8"))
        print("src/Baby9.snp matches jar:", s2 == store)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
