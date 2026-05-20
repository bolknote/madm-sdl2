#!/usr/bin/env python3
"""Build cambridge_fib.store and m1sim_factor.store from cached upstream zips."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from convert_baby_source import parse_snp_text, write_store

PROGRAMS = Path(__file__).resolve().parent.parent / "programs"
UP = Path(__file__).resolve().parent / "upstream"


def snp_from_zip(zip_path: Path, name: str) -> tuple[list[int], int | None]:
    data = subprocess.check_output(["unzip", "-p", str(zip_path), name]).decode()
    return parse_snp_text(data)


def main() -> int:
    java = UP / "JavaBaby.zip"
    m1 = UP / "m1sim.zip"
    if not java.is_file():
        print("missing", java, "— run ./download_upstream.sh first", file=sys.stderr)
        return 1
    if not m1.is_file():
        print("missing", m1, "— run ./download_upstream.sh first", file=sys.stderr)
        return 1

    extras = [
        (java, "FIB.SNP", "cambridge_fib.store",
         "Fibonacci (Simon Moore / Cambridge JavaBaby)",
         "https://www.cl.cam.ac.uk/teaching/0910/ECAD+Arch/files/JavaBaby.zip"),
        (m1, "FACTOR.SNP", "m1sim_factor.store",
         "Factor example (Andy Molyneux M1SIM FACTOR.ASM)",
         "https://www.cs.man.ac.uk/CCS/Archive/simulators/SSEM/m1sim.zip"),
    ]
    for zpath, snp, out, title, url in extras:
        store, ci = snp_from_zip(zpath, snp)
        write_store(PROGRAMS / out, title, url, store, ci_start=ci)
        print("wrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
