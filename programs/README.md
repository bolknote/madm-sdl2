# Programs for MADM

Williams-tube store images for the Manchester Mark I prototype / Manchester
Baby / SSEM simulator. Each `.store` file is a 32-line, 32-bit memory snapshot;
bits are displayed least-significant bit first, as on the original tube display.

## Quick start

Run a store image in the SDL simulator:

```bash
cd ..   # MADM.English
make
./madm -f programs/davidsharp_primegen.store
./madm -f programs/kilburn_july48.store
```

Press **Enter** to run and **s** to single-step.

Run the Python emulator without a window:

```bash
python3 ../examples/manchester_baby/madm_sim.py -f programs/cambridge_fib.store --run --dump
```

## Store format

- `@N value` loads `value` into store line `N` (`0` to `31`).
- Lines without `@N` are loaded sequentially.
- `# ci-start -1` sets CI to `-1` after loading, so the first fetch executes line `0`.
- `#` starts a comment line; values may be decimal, signed decimal, or `0x` hex.

## Suggested first runs

| File | Why start here |
|------|----------------|
| `kilburn_july48.store` | The historical highest-factor routine bundled with the original MADM lineage |
| `davidsharp_primegen.store` | Interactive prime generator; restart after each STOP |
| `cambridge_fib.store` | Short Fibonacci run with an easy numeric check |
| `ccs_all1test.store` | Compact diagnostic covering all opcodes |
| `show67.store` | Local visual demo that draws `67` after execution |

## Catalog

### Historical and reference programs

| File | What it does | Source / note |
|------|----------------|---------------|
| `kilburn_july48.store` | Highest proper factor, amended **18 July 1948** listing; reliability run **21 June 1948** | Geoff Tootill notebook; [Computer50 notes](https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/notes.html#reconsprog1); Lee Wittenberg MADM demo |
| `m1sim_factor.store` | Kilburn-style factorization demo | `FACTOR.SNP` in [Manchester CCS m1sim.zip](https://www.cs.man.ac.uk/CCS/Archive/simulators/SSEM/m1sim.zip), Andy Molyneux M1SIM, 1996 |
| `ccs_factorct.store` | Full factor-run layout from volunteer guide (`FACTORCT.SNP` text) | [CCS Technical Introduction v4.0 PDF](https://computerconservationsociety.org/ssemvolunteers/volunteers/A%20Technical%20Introduction%20To%20Programming%20the%20Baby%20v4.0.pdf) |
| `ccs_prog1_989.store` | Same code as `ccs_factorct.store` with `@23=-989`, `@24=988` | About 20k steps |
| `cambridge_fib.store` | Fibonacci sequence | `FIB.SNP` in [Cambridge JavaBaby.zip](https://www.cl.cam.ac.uk/teaching/0910/ECAD+Arch/files/JavaBaby.zip), Simon Moore lectures |
| `davidsharp_baby9.store` | Marquee display from a 2008 photo-realistic simulator example | `Baby9.snp` in [ssem.zip](https://www.davidsharp.com/baby/ssem.zip) / [src.zip](https://www.davidsharp.com/baby/src.zip); related to `slide9.snp` but not identical |

### Computer 50 competition / David Sharp archive

Converted from [David Sharp program SVN](https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program/).
These are the same 12 programs listed by MAME as `ssem_quik`.

| File | What it does | Author / note | Upstream |
|------|----------------|---------------|----------|
| `davidsharp_noodletimer.store` | 3-minute noodle timer | Yasuaki Watanabe, winner | `noodletimer.snp` |
| `davidsharp_primegen.store` | Prime generator; restart after each STOP | Bas Wijnen, runner-up | `primegen.asm` |
| `davidsharp_medclock.store` | “Medieval” clock on lines 30-31 | John Deane, runner-up | `medclock.snp` |
| `davidsharp_diffeqt.store` | Parabola / difference equation plot | Magnus Olsson, runner-up | `diffeqt.asm` |
| `davidsharp_intdiv.store` | Integer division | Brendan Campbell, UK schools prize | `intdiv.snp` |
| `davidsharp_nightmare.store` | Baby chasing Tom Kilburn | Competition entry, Hurley per Computer50 | `nightmare.snp` |
| `davidsharp_virpet.store` | Virtual pet, Tamagotchi-style | Achut Reddy, competition entry | `virpet.asm` |
| `davidsharp_longdiv2.store` | Long division | Turing | `longdiv2.snp` |
| `davidsharp_slide9.store` | Sliding / marquee display | Keith Wood | `slide9.snp` |
| `davidsharp_hcf.store` | HCF of 3142 and 2178 (co-prime) | Geoff Tootill | `hcf.asm` |
| `davidsharp_hfr989.store` | HCF routine for 989 -> 43 | Tom Kilburn | `hfr989.asm` |
| `davidsharp_flash.store` | Flash / timing pattern | Ken Turner, replica team | `flash.asm` |

Also present in [baby.zip](https://www.davidsharp.com/baby/baby.zip) as the same
`programs/` tree.

### CCS / MOSI replica diagnostics

Reconstructed from bit dumps in [Baby Functions Diagnostic Test Files -
Analysis (PDF)](https://computerconservationsociety.org/ssemvolunteers/volunteers/Baby%20Functions%20Diagnostic%20Test%20Files%20-%20Analysis.1.0.pdf).
These programs were used on the working Baby replica and are not part of the
1998 competition.

| File | What it tests |
|------|---------------|
| `ccs_jmp1test.store` | **JMP** (`CI <- store line`) |
| `ccs_jrp1test.store` | **JRP** / relative jump |
| `ccs_ldn1test.store` | **LDN** |
| `ccs_sto1test.store` / `ccs_sto2test.store` | **STO** |
| `ccs_sub1test.store` | **SUB** |
| `ccs_cmp1test.store` / `ccs_cmp2test.store` | **CMP**, skip when `A >= 0` |
| `ccs_all1test.store` | Combined opcode test; line 16 should count down from `1024` to `-1` |

Regenerate with `python3 ../scripts/convert_ccs_diagnostic.py`; it needs
`scripts/upstream/ccs/diagnostic.txt` generated with `pdftotext` from the PDF.

### HASE, JsSSEM, Rosetta, and CCS guide conversions

Converted by `python3 ../scripts/convert_program_hunt.py`.

| File | What it does | Source |
|------|----------------|--------|
| `hase_insn_demo.store` | Exercises all SSEM opcodes (short demo) | Edinburgh [mu_baby_v4.1.zip](https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/ssem/mu_baby_v4.1.zip), program 1 |
| `hase_highest_factor.store` | Highest-factor program, 18 July 1948 layout | Same HASE model, program 2; HASE loader maps instructions to lines 1+ |
| `hase_third_demo.store` | Third built-in HASE demo (CRT / store pattern) | Same HASE model, program 3 |
| `jsssem_fibo40.store` | Fibonacci: 40th term in A (`102334155`) | [JsSSEM](http://www.edmundgriffiths.com/jsssem.html), base-32 tape `fib` |
| `jsssem_prisoner.store` | Playable iterated Prisoner’s Dilemma (Tit-for-Tat opponent) | JsSSEM tape `prisoner` |
| `jsssem_addition.store` | Add two values in store | JsSSEM tape `addition` |
| `jsssem_multiply.store` | Multiply via repeated subtraction | JsSSEM tape `multip` |
| `jsssem_wheeler.store` | Wheeler jump subroutine demo | JsSSEM tape `wheeler` |
| `rosetta_stop.store` | Minimal program: STOP at line 0 | [Rosetta Code - Empty program](https://rosettacode.org/wiki/Empty_program#SSEM) |
| `rosetta_empty_loop.store` | All-zero store -> infinite `goto 1` | Same Rosetta page |
| `rosetta_hello_graphical.store` | “Hello” drawn in Williams-tube bits | [Rosetta Code - Hello world/Graphical](https://rosettacode.org/wiki/Hello_world/Graphical#SSEM) |

HASE note: the model loads instructions at store line *i+1* and trailing
`INPUT.data_mem` words after the last instruction (see `input.hase` in the zip).
Parameter `Program=4` is defined in the model but slot 4 is empty in
`mu_baby_v4.1.zip`.

### NevynUK / Mark Stevens

Source: [NevynUK/ManchesterBaby](https://github.com/NevynUK/ManchesterBaby).
`python3 ../scripts/convert_nevynuk.py` reads `Source/SSEMPrograms/*.ssem`
colon listings (`NN: MNEM operand`; `SKN` = `CMP`, `HLT` = `STOP`, `BNUM` for
binary constants).

| File | What it does | Notes |
|------|----------------|-------|
| `nevynuk_add.store` | 10 + 5 -> A = 15 | Blog “small test” |
| `nevynuk_hcf989.store` | HCF for **989** | Same listing as blog / `hfr989.ssem`; layout differs from `davidsharp_hfr989.store` |
| `nevynuk_hcf1.store` | Factor demo (`N = -35`) | `HCF1.ssem` |
| `nevynuk_hcf2.store` | Euclidean HCF, large constants | `HCF2.ssem` |
| `nevynuk_turing_longdiv.store` | Turing long division (`A=36`, `B=20`, quotient at `@28`) | `TuringLongDivision.ssem`; same 32 words as [pico-baby-if `program.c`](https://github.com/krisjdev/pico-baby-if/blob/main/program.c), [comparch `TuringLongDivision.logisimRAMImage`](https://gitlab.com/charles.fox/comparch/-/blob/main/chapter07/TuringLongDivision.logisimRAMImage), and the **32 LSB-left lines** in Charles Fox, *Computer Architecture* ([dokumen.pub mirror](https://dokumen.pub/computer-architecture-from-the-stone-age-to-the-quantum-age-9781718502864-9781718502871.html) — search “machine code for Turing”); Tiny Tapeout expects **STOP (`0xe0000000`) at line 28** after run |
| `nevynuk_add.store` | 10 + 5 → **15** in A (`LDN 20`, `SUB 21`, `STO 22`, `LDN 22`, `STOP`) | Mark Stevens / ManchesterBaby.computer sample format (`Add.ssem`) |
| `nevynuk_jmp_test.store` | JMP self-test | `Factor95.ssem` (misleading name) |
| `nevynuk_primes.store` | Prime generator | Overlaps `davidsharp_primegen` |
| `nevynuk_parabola.store` | Parabola plot | Overlaps `davidsharp_diffeqt` |
| `nevynuk_nightmare.store` | Nightmare | Overlaps `davidsharp_nightmare` |
| `nevynuk_intdiv.store` | Integer division | Overlaps `davidsharp_intdiv` |
| `nevynuk_clock.store` | Clock | Overlaps `davidsharp_medclock` |
| `nevynuk_3minutes.store` | 3-minute timer | Overlaps `davidsharp_noodletimer` |

The C++/NuttX tree also ships the same `.ssem` files under
`Source/CPP/.../SSEMApps/`.

### BabyPing

Source: [hrvach/babyping](https://github.com/hrvach/babyping). BabyPing stores
32-bit LSB-left lines (`int(line[::-1], 2)` in the upstream code). Regenerate
with `python3 ../scripts/convert_more_sources.py`.

| File | What it does | Relation to existing catalog |
|------|----------------|------------------------------|
| `babyping_scroll.store` | Scrolling CRT pattern | Unique, not `davidsharp_slide9` |
| `babyping_kilburn.store` | Bit dump named “kilburn” upstream | Same bytes as `davidsharp_nightmare`, not the factor program |
| `babyping_parabola.store` | Parabola plot | Same as `davidsharp_diffeqt` |
| `babyping_noodle.store` | Noodle timer | Same as `davidsharp_noodletimer` |
| `babyping_intdiv.store` | Integer division | Same as `davidsharp_intdiv` |
| `babyping_clock.store` | Clock display | Same as `davidsharp_medclock` |

### gobaby

Source: [jcla1/gobaby](https://github.com/jcla1/gobaby).

| File | What it does | Relation to existing catalog |
|------|----------------|------------------------------|
| `gobaby_factor.store` | Factor 2^18, Joseph Adams listing | Same as `ccs_factorct` and the [Retrocomputing SE](https://retrocomputing.stackexchange.com/a/2869) / [gobaby `examples/factor.asm`](https://github.com/jcla1/gobaby/blob/main/examples/factor.asm) listing (`gobaby -t -l 27 -p=f`) |
| `gobaby_primegen.store` | Chainable prime generator | Same as `davidsharp_primegen` |
| `gobaby_simple_calc.store` | 5 - 3 -> result in line 9 | Unique, 5 steps |

### Andy Bower sim / Python (round 2)

Sources: [manchester-baby-sim](https://github.com/andy-bower/manchester-baby-sim),
[ManchesterBabyPython](https://github.com/andy-bower/ManchesterBabyPython).
Regenerate with `python3 ../scripts/convert_round2.py` (numbered `.asm` only;
skips catalog duplicates).

| File | What it does | Relation to existing catalog |
|------|----------------|------------------------------|
| `bower_sim_fibonacci.store` | Fibonacci to index in line 29 (default 46) | David Tarnoff tutorial layout; not the same bytes as `cambridge_fib` |
| `bower_mpy_jrptest.store` | JRP self-test; stops with **A = 2** | Numbered listing (`JRPTest.asm`); differs from `babyutils_test_jrp` |
| `bower_mpy_cirollover.store` | CI rollover / STOP exercise | `CIRollover.asm` |

`convert_round2.py` also skips byte-identical copies of `ccs_factorct`,
`davidsharp_primegen`, `nevynuk_*`, and Turing long division already in
`nevynuk_turing_longdiv.store`. CCS-style `samples/ssem/tests/*.snp` in the sim
repo match the existing `ccs_*test.store` set.

### babyutils toolchain tests (round 3)

Source: [andy-bower/babyutils](https://github.com/andy-bower/babyutils) `test/`.
Regenerate with `python3 ../scripts/convert_round3.py`, which uses
`parse_babyutils_asm()` (labels, `EJA`, implicit line addresses). Skips
`macro.asm`, `relative.asm`, `subroutines.asm` (extra syntax), and
`lddiv.asm` / `lddiv-pic.asm` (same bytes as `nevynuk_turing_longdiv`).

| File | What it does | Notes |
|------|----------------|-------|
| `babyutils_test_jmp.store` | **JMP** via `EJA` trampoline (`test-jmp.asm`) | Check words at lines 28-31 |
| `babyutils_test_jrp.store` | **JRP** via `EJA` (`test-jrp.asm`) | Different layout from `bower_mpy_jrptest` |
| `babyutils_test_count31.store` | Count down with **SKN** / **HLT** at 2^31 wrap | `test-count31.asm` |
| `babyutils_test_count_forever.store` | Infinite subtract loop (no **HLT**) | `test-count-forever.asm` |

### Rust `baby-emulator` / SSEMBabyEmulator

Layouts are taken from `core/mod.rs` and assembler docs. Crates.io `0.2.1`
source does not build as-is because of format-string typos.

| File | What it does |
|------|----------------|
| `baby_rust_add5.store` | `BabyModel::new_example_program()`; 5+5 -> A = -10 display |
| `baby_rust_countdown.store` | README loop: 10 down to -1, about 34 steps |

### Local demos

| File | What it does | Source |
|------|----------------|--------|
| `show67.store` | Draws bitmap `67` on store rows when run (not pre-painted) | Written for this MADM port |
| `bolk_anim.store` | Reveals `BOLK` row by row from masked row data | Written for this MADM port |

### Checked but not added as new programs

| Source | Status |
|--------|--------|
| [krisjdev/pico-baby-if](https://github.com/krisjdev/pico-baby-if) | `program.c` Turing long division RAM = `nevynuk_turing_longdiv.store`; Tiny Tapeout test expects **0xe0000000** at store line **28** after run (initial image has `0` there) |
| [charles.fox/comparch](https://gitlab.com/charles.fox/comparch) ch07 | `TuringLongDivision.asm`, `babyAssemble.py`, `TuringLongDivision.logisimRAMImage` — same 32 words as above |
| Fox book machine-code dump | dokumen.pub HTML embeds 32×32-bit lines after “machine code for Turing”; verified = `nevynuk_turing_longdiv` (`scripts/upstream/fox-book/TuringLongDivision.machine.txt`) |
| [Retrocomputing SE #2869](https://retrocomputing.stackexchange.com/a/2869) | Full `factor.asm` = `gobaby_factor` / `ccs_factorct` (cached as `scripts/upstream/retro-factor/factor.asm`) |
| Mark Stevens blog sample | `Add.ssem` (10+5→15) = `nevynuk_add.store`; `hfr989.ssem` = `nevynuk_hcf989` (layout differs from `davidsharp_hfr989`) |
| [open-simh/simh](https://github.com/open-simh/simh) | `SSEM/` supports `LOAD`/`DUMP` of `.st` store files and mnemonic entry, but ships no sample `.st` programs |
| [diy-ic/tt-manchester-baby](https://github.com/diy-ic/tt-manchester-baby) | `test/test.py` init RAM is Turing long division, identical to `nevynuk_turing_longdiv.store` |
| [EMF Manchester Baby](https://em.ulat.es/machines/ManchesterBaby/) | HTTPS fetch failed here; retry manually for embedded JS demos |
| MAME `ssem_quik.zip` | archive.org returned HTTP 401/500; bytes match David Sharp SVN via `ssem_quik.xml` CRCs |
| NevynUK Python `Assembler()` | Does not accept `BNUM` lines, only `BIN` / `BINS`; use this repository's converter instead |

## Provenance notes

### MAME `ssem_quik`

MAME 0.226 ([whatsnew](https://www.mamedev.org/releases/whatsnew_0226.txt))
lists working quickload software for `ssem`: DIFFEQT, FLASH, HCF, HFR989,
INTDIV, LONGDIV2, MEDCLOCK, NIGHTMARE, Noodle Timer, PRIMEGEN, Slide Show, and
Virtual Pet. The list is credited to Robbbert, with “all from the collection” on
Virtual Pet.

The software-list ROM pack is `ssem_quik.zip` on archive.org, but the May 2026
fetch returned HTTP 401/500 here. The authoritative metadata is still
[hash/ssem_quik.xml](https://raw.githubusercontent.com/mamedev/mame/master/hash/ssem_quik.xml).

CRC checks show that raw bytes from [David Sharp SVN](https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program/)
match MAME’s CRC32 values for `diffeqt.asm`, `noodletimer.snp`, `slide9.snp`,
`virpet.asm`, and the rest of the 12-program set. So MAME’s “collection” is the
same set already represented by `davidsharp_*.store`, not a separate hidden
corpus.

MAME git notes: commits
[186db4f6](https://github.com/mamedev/mame/commit/186db4f627),
[6f8aece](https://github.com/mamedev/mame/commit/6f8aece4a4), and
[878a16d](https://github.com/mamedev/mame/commit/878a16dda1) touch
`hash/ssem_quik.xml`. The phrase “all from the collection” appears in
[95202d5](https://github.com/mamedev/mame/commit/95202d5e3e), where `ssem.cpp`
hooks the `ssem_quik` software list.

### Archive checks

| Archive | URL | Programs inside |
|---------|-----|-----------------|
| David Sharp SVN | `.../baby/program/` | 12 competition files; complete public web set |
| David Sharp `baby.zip` | [baby.zip](https://www.davidsharp.com/baby/baby.zip) | Same 12 plus PDF docs |
| David Sharp `ssem.zip` / `src.zip` | [davidsharp.com/baby](https://www.davidsharp.com/baby/) | `ssem.jar` menu: Baby9, diffeqt, noodletimer, primegen, virpet |
| Manchester `m1sim.zip` | [CCS SSEM](https://www.cs.man.ac.uk/CCS/Archive/simulators/SSEM/) | `FACTOR` plus DOS simulator |
| Cambridge `JavaBaby.zip` etc. | `.../ECAD+Arch/files/` (0910 and 1011) | 7 SNPs: FIB plus renamed competition snapshots |
| Computer50 mirror | [prog98](https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/prog98/) | About 128 entries described; no bulk download |
| Digital60 2008 contest | `.../Digital60/Digital60-AliceCompetition/` | Live URL 404; Wayback prize pages link missing entry zips; CDX has the same David Sharp emulator zips |
| CCS SSEM emulators | [computerconservationsociety.org/emu/ssem/](https://www.computerconservationsociety.org/emu/ssem/) | `madm.zip` = Lee Wittenberg source; `wmadm.zip` = Windows build plus `.mdm` samples |
| CCS diagnostic PDF | [volunteers analysis PDF](https://computerconservationsociety.org/ssemvolunteers/volunteers/Baby%20Functions%20Diagnostic%20Test%20Files%20-%20Analysis.1.0.pdf) | Nine `*Test.snp` programs -> `ccs_*test.store` |

Not found as downloadable `.snp` files: `PROG1.SNP` (989 demo, described in a
guide but no public snapshot), `slidex.snp` (museum demo name in refman), and
the remaining Computer50 `prog98` submissions. `FACTORCT.SNP` is reproduced as
`ccs_factorct.store` from the CCS volunteer guide PDF; it may differ slightly
from the MOSI file because the guide omits ignored bit-5 flags.

For more material, try
[compsci-history@listserv.manchester.ac.uk](mailto:compsci-history@listserv.manchester.ac.uk),
MOSI, or the Manchester archive.

## Regenerating

The conversion scripts live in `../scripts/`. Maintainer workflow:

```bash
cd ../scripts
./download_upstream.sh
python3 convert_program_hunt.py
python3 convert_nevynuk.py
python3 convert_ccs_diagnostic.py
python3 convert_more_sources.py
python3 convert_round2.py
python3 convert_round3.py
python3 convert_fox_retro.py
```

See `../scripts/README.md` for script-specific notes.

The catalog currently ships **70** `.store` files (32 lines each).
