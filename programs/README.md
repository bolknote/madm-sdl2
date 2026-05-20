# Programs for MADM

Williams-tube store images (32 lines × 32 bits, LSB on the left) for the Manchester Mark I prototype simulator.

## Run

```bash
cd ..   # MADM.English
make
./madm -f programs/davidsharp_primegen.store
./madm -f programs/kilburn_july48.store
```

Press **Enter** to run, **s** to step. Python emulator (no window):

```bash
python3 ../examples/manchester_baby/madm_sim.py -f programs/cambridge_fib.store --run --dump
```

## Store format

- `@N value` — load word into store line `N` (0–31)
- `# ci-start -1` — after load, CI = −1 so the first fetch executes line 0
- `#` comments; values decimal, `0x` hex, or signed decimal

---

## Program catalog

### Historical

| File | What it does | Source |
|------|----------------|--------|
| `kilburn_july48.store` | Highest proper factor (amended **18 July 1948** listing); reliability run **21 June 1948** | Geoff Tootill notebook; [Computer50 notes](https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/notes.html#reconsprog1); Lee Wittenberg MADM demo |

### Computer 50 competition (1998) — David Sharp archive

Converted from [David Sharp program SVN](https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program/) (same 12 as MAME `ssem_quik`):

| File | What it does | Author / note | Upstream |
|------|----------------|---------------|----------|
| `davidsharp_noodletimer.store` | 3-minute noodle timer | Yasuaki Watanabe — **winner** | `noodletimer.snp` |
| `davidsharp_primegen.store` | Prime generator (restart after each STOP) | Bas Wijnen — runner-up | `primegen.asm` |
| `davidsharp_medclock.store` | “Medieval” clock on lines 30–31 | John Deane — runner-up | `medclock.snp` |
| `davidsharp_diffeqt.store` | Parabola / difference equation plot | Magnus Olsson — runner-up | `diffeqt.asm` |
| `davidsharp_intdiv.store` | Integer division | Brendan Campbell — UK schools prize | `intdiv.snp` |
| `davidsharp_nightmare.store` | Baby chasing Tom Kilburn | Competition entry (Hurley per Computer50) | `nightmare.snp` |
| `davidsharp_virpet.store` | Virtual pet (Tamagotchi-style) | Achut Reddy — competition entry | `virpet.asm` |
| `davidsharp_longdiv2.store` | Long division | Turing | `longdiv2.snp` |
| `davidsharp_slide9.store` | Sliding / marquee display | Keith Wood | `slide9.snp` |
| `davidsharp_hcf.store` | HCF of 3142 and 2178 (co-prime) | Geoff Tootill | `hcf.asm` |
| `davidsharp_hfr989.store` | HCF routine for 989 → 43 | Tom Kilburn | `hfr989.asm` |
| `davidsharp_flash.store` | Flash / timing pattern | Ken Turner, replica team | `flash.asm` |

Also in [baby.zip](https://www.davidsharp.com/baby/baby.zip) (2001 emulator bundle) as the same `programs/` tree.

### Other published snapshots

| File | What it does | Source |
|------|----------------|--------|
| `davidsharp_baby9.store` | Marquee display (2008 photo-realistic simulator example) | `Baby9.snp` in [ssem.zip](https://www.davidsharp.com/baby/ssem.zip) / [src.zip](https://www.davidsharp.com/baby/src.zip); related to `slide9.snp` but **not identical** |
| `cambridge_fib.store` | Fibonacci sequence | `FIB.SNP` in [Cambridge JavaBaby.zip](https://www.cl.cam.ac.uk/teaching/0910/ECAD+Arch/files/JavaBaby.zip) (Simon Moore lectures; not the 1998 competition) |
| `m1sim_factor.store` | Kilburn-style factorization demo | `FACTOR.SNP` in [Manchester CCS m1sim.zip](https://www.cs.man.ac.uk/CCS/Archive/simulators/SSEM/m1sim.zip) (Andy Molyneux M1SIM, 1996) |

### CCS / MOSI replica diagnostics (function tests)

Reconstructed from bit dumps in [Baby Functions Diagnostic Test Files — Analysis (PDF)](https://computerconservationsociety.org/ssemvolunteers/volunteers/Baby%20Functions%20Diagnostic%20Test%20Files%20-%20Analysis.1.0.pdf) (SSEM volunteers). Used on the working Baby replica; not part of the 1998 competition.

| File | What it does |
|------|----------------|
| `ccs_jmp1test.store` | Tests **JMP** (CI ← store line) |
| `ccs_jrp1test.store` | Tests **JRP** (relative jump) |
| `ccs_ldn1test.store` | Tests **LDN** |
| `ccs_sto1test.store` / `ccs_sto2test.store` | Tests **STO** |
| `ccs_sub1test.store` | Tests **SUB** |
| `ccs_cmp1test.store` / `ccs_cmp2test.store` | Tests **CMP** (skip when A ≥ 0) |
| `ccs_all1test.store` | **Combined** test of all opcodes; line 16 should count down from 1024 to −1 |

Regenerate: `python3 ../scripts/convert_ccs_diagnostic.py` (needs `scripts/upstream/ccs/diagnostic.txt` from `pdftotext` on the PDF).

### Program-hunt sources (HASE, JsSSEM, Rosetta, CCS guide)

Converted by `python3 ../scripts/convert_program_hunt.py` (cache: `scripts/upstream/hase/`, `jsssem.html` from Wayback).

| File | What it does | Source |
|------|----------------|--------|
| `hase_insn_demo.store` | Exercises all SSEM opcodes (short demo) | Edinburgh [mu_baby_v4.1.zip](https://www.icsa.inf.ed.ac.uk/research/groups/hase/models/ssem/mu_baby_v4.1.zip) program 1 |
| `hase_highest_factor.store` | Highest-factor program (18 July 1948 layout; HASE loader maps insn to lines 1+) | Same HASE model, program 2 |
| `hase_third_demo.store` | Third built-in HASE demo (CRT / store pattern) | Same, program 3 |
| `jsssem_fibo40.store` | Fibonacci: 40th term in A (102334155) | [JsSSEM](http://www.edmundgriffiths.com/jsssem.html) base-32 tape `fib` |
| `jsssem_prisoner.store` | Playable iterated Prisoner’s Dilemma (Tit-for-Tat opponent) | JsSSEM tape `prisoner` |
| `jsssem_addition.store` | Add two values in store | JsSSEM tape `addition` |
| `jsssem_multiply.store` | Multiply via repeated subtraction | JsSSEM tape `multip` |
| `jsssem_wheeler.store` | Wheeler jump subroutine demo | JsSSEM tape `wheeler` |
| `rosetta_stop.store` | Minimal program: STOP at line 0 | [Rosetta Code — Empty program](https://rosettacode.org/wiki/Empty_program#SSEM) |
| `rosetta_empty_loop.store` | All-zero store → infinite `goto 1` | Same |
| `rosetta_hello_graphical.store` | “Hello” drawn in Williams-tube bits | [Rosetta Code — Hello world/Graphical](https://rosettacode.org/wiki/Hello_world/Graphical#SSEM) |
| `ccs_factorct.store` | Full factor-run layout from volunteer guide (**FACTORCT.SNP** text) | [CCS Technical Introduction v4.0 PDF](https://computerconservationsociety.org/ssemvolunteers/volunteers/A%20Technical%20Introduction%20To%20Programming%20the%20Baby%20v4.0.pdf) |

HASE note: the model loads instructions at store line *i+1* and trailing `INPUT.data_mem` words after the last instruction (see `input.hase` in the zip). Parameter `Program=4` is defined in the model but slot 4 is empty in `mu_baby_v4.1.zip`.

### NevynUK / Mark Stevens ([ManchesterBaby](https://github.com/NevynUK/ManchesterBaby))

`python3 ../scripts/convert_nevynuk.py` reads `Source/SSEMPrograms/*.ssem` (colon listing: `NN: MNEM operand`, `SKN` = `CMP`, `HLT` = `STOP`, `BNUM` for binary constants).

| File | What it does | Notes |
|------|----------------|--------|
| `nevynuk_add.store` | 10 + 5 → A = 15 | Blog “small test” |
| `nevynuk_hcf989.store` | HCF for **989** | Same listing as blog / `hfr989.ssem`; layout differs from `davidsharp_hfr989.store` |
| `nevynuk_hcf1.store` | Factor demo (N = −35) | `HCF1.ssem` |
| `nevynuk_hcf2.store` | Euclidean HCF (large constants) | `HCF2.ssem` |
| `nevynuk_turing_longdiv.store` | Turing **long division** (A=36, B=20 → quotient @28) | From `TuringLongDivision.ssem` / *Computer Architecture* scan; upstream `.ssem` uses `BNUM` (not in their Python assembler); check quotient in MADM |
| `nevynuk_jmp_test.store` | JMP self-test | `Factor95.ssem` (misleading name) |
| `nevynuk_primes.store` | Prime generator | Overlaps `davidsharp_primegen` (verify if identical) |
| `nevynuk_parabola.store` | Parabola plot | Overlaps `davidsharp_diffeqt` |
| `nevynuk_nightmare.store` | Nightmare | Overlaps `davidsharp_nightmare` |
| `nevynuk_intdiv.store` | Integer division | Overlaps `davidsharp_intdiv` |
| `nevynuk_clock.store` | Clock | Overlaps `davidsharp_medclock` |
| `nevynuk_3minutes.store` | 3-minute timer | Overlaps `davidsharp_noodletimer` |

C++/NuttX tree also ships the same `.ssem` files under `Source/CPP/.../SSEMApps/`.

### BabyPing ([hrvach/babyping](https://github.com/hrvach/babyping))

32-bit **LSB-left** lines (same as Williams tube); `convert_extra_hunt.py`.

| File | What it does | vs existing |
|------|----------------|-------------|
| `babyping_scroll.store` | Scrolling CRT pattern | **unique** |
| `babyping_kilburn.store` | Factor bit-dump | Differs from `kilburn_july48.store` (other layout) |
| `programs/parabola.ssem` etc. | — | **Identical** to `davidsharp_diffeqt`, `noodletimer`, `intdiv`, `medclock` |

### Rust `baby-emulator` / [SSEMBabyEmulator](https://github.com/jasonalexander-ja/SSEMBabyEmulator)

| File | What it does |
|------|----------------|
| `baby_rust_add5.store` | `BabyModel::new_example_program()` (5+5 → A=−10 display) |
| `baby_rust_countdown.store` | README loop: 10 down to −1 (~34 steps) |

Crates.io **0.2.1** source does not build as-is (format-string typos); layouts taken from `core/mod.rs` + assembler docs.

### CCS PROG1 (989 demo)

| File | What it does |
|------|----------------|
| `ccs_prog1_989.store` | Same code as `ccs_factorct.store` with @23=−989, @24=988 (~20k steps) |

### Not harvested (this pass)

| Source | Status |
|--------|--------|
| [EMF Manchester Baby](https://em.ulat.es/machines/ManchesterBaby/) | HTTPS fetch failed here; retry manually for embedded JS demos |
| MAME `ssem_quik.zip` | archive.org **401**; bytes match David Sharp SVN via `ssem_quik.xml` CRCs |
| NevynUK Python `Assembler()` | Does not accept `BNUM` lines (only `BIN`/`BINS`); use our converter instead |

### Local demo

| File | What it does | Source |
|------|----------------|--------|
| `show67.store` | Draws bitmap «67» on store rows when run (not pre-painted) | Written for this MADM port |
| `bolk_anim.store` | Reveals `BOLK` row by row from masked row data | Written for this MADM port |

---

## Sources (where the `.store` files come from)

### MAME `ssem_quik` — “the collection” (12 programs)

MAME 0.226 ([whatsnew](https://www.mamedev.org/releases/whatsnew_0226.txt)) lists working quickload software for `ssem`: DIFFEQT, FLASH, HCF, HFR989, INTDIV, LONGDIV2, MEDCLOCK, NIGHTMARE, Noodle Timer, PRIMEGEN, Slide Show, Virtual Pet — credited to **Robbbert**, with **“all from the collection”** on Virtual Pet.

The software-list ROM pack is [`ssem_quik.zip`](https://archive.org/download/mame-sl/mame-sl/ssem_quik.zip) on archive.org (Spludlow indexes it as a MAME software-list set). **May 2026:** that ZIP returned HTTP 401/500 here; the authoritative metadata is still [hash/ssem_quik.xml](https://raw.githubusercontent.com/mamedev/mame/master/hash/ssem_quik.xml).

**CRC check:** raw bytes from [David Sharp SVN](https://davidsharp.com/publicsvn/baby/source/com/davidsharp/baby/program/) match MAME’s CRC32 for `diffeqt.asm`, `noodletimer.snp`, `slide9.snp`, `virpet.asm`, etc. So “the collection” is the **same 12 files** already in `davidsharp_*.store`, not a separate hidden corpus of 128 programs.

**MAME git (Robbbert, 2020-10-17/18):** only three commits touch `hash/ssem_quik.xml` — [186db4f6](https://github.com/mamedev/mame/commit/186db4f627) creates the list (all 12 CRCs at once, no source URL), [6f8aece](https://github.com/mamedev/mame/commit/6f8aece4a4) adds virpet usage text, [878a16d](https://github.com/mamedev/mame/commit/878a16dda1) SPDX housekeeping. The phrase *“all from the collection”* is in commit [95202d5](https://github.com/mamedev/mame/commit/95202d5e3e) (`ssem.cpp`: hook `ssem_quik` software list). The separate ROM zip `ssem_quik.zip` was not found in the MAME source tree; archive.org copy failed here (401/500).

### Other archives (checked)

| Archive | URL | Programs inside |
|---------|-----|-----------------|
| David Sharp SVN | `…/baby/program/` | 12 competition files (complete public web set) |
| David Sharp **baby.zip** | [baby.zip](https://www.davidsharp.com/baby/baby.zip) | Same 12 + PDF docs |
| David Sharp **ssem.zip** / **src.zip** | [davidsharp.com/baby/](https://www.davidsharp.com/baby/) | `ssem.jar` menu: Baby9, diffeqt, noodletimer, primegen, virpet (**5** only) |
| Manchester **m1sim.zip** | [CCS SSEM](https://www.cs.man.ac.uk/CCS/Archive/simulators/SSEM/) | **FACTOR** only (+ DOS simulator) |
| Cambridge **JavaBaby** etc. | `…/ECAD+Arch/files/JavaBaby.zip` (0910 and 1011) | 7 SNPs: FIB + renamed competition snapshots |
| Computer50 mirror | [prog98](https://curation.cs.manchester.ac.uk/computer50/www.computer50.org/mark1/prog98/) | ~128 entries described; **no bulk download** |
| Digital60 2008 contest | `…/Digital60/Digital60-AliceCompetition/` | Live URL **404**; prizes HTML (Wayback 2010) links `entries/Winner/Winner.zip` but file **404**; CDX has [Digital60/Baby/ssem/*.zip](https://web.archive.org/web/20120329034512/http://www.cs.manchester.ac.uk/Digital60/Baby/ssem/ssem.zip) (same as davidsharp.com) |
| CCS **SSEM emulators** | [computerconservationsociety.org/emu/ssem/](https://www.computerconservationsociety.org/emu/ssem/) | [madm.zip](https://www.computerconservationsociety.org/emu/ssem/madm.zip) = Lee Wittenberg **source** (same lineage as this port); [wmadm.zip](https://www.computerconservationsociety.org/emu/ssem/wmadm.zip) = Windows build + `.mdm` samples only |
| CCS diagnostic PDF | [volunteers analysis PDF](https://computerconservationsociety.org/ssemvolunteers/volunteers/Baby%20Functions%20Diagnostic%20Test%20Files%20-%20Analysis.1.0.pdf) | Nine `*Test.snp` programs → `ccs_*test.store` |

**Not found as downloadable `.snp` files:** `PROG1.SNP` (989 demo — guide describes it but no public snapshot); `slidex.snp` (museum demo name in refman); remaining ~120× prog98 submissions. **`FACTORCT.SNP`** bit dump is reproduced as `ccs_factorct.store` from the CCS volunteer guide PDF (may differ slightly from MOSI file: guide omits ignored bit 5 flags).

For more material: [compsci-history@listserv.manchester.ac.uk](mailto:compsci-history@listserv.manchester.ac.uk), MOSI / Manchester archive.

Regenerating `.store` files from upstream (maintainers): see `../scripts/README.md`.
