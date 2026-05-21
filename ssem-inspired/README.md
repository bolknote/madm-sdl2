# SSEM-inspired and non–32×32 programs

Material that is **related** to the Manchester Baby / SSEM story but **not** loadable as
MADM `programs/*.store` (32 lines × 32 bits, Williams-tube layout). Kept here so it
does not mix with the main Baby corpus in `programs/README.md`.

## C88 (Daniel Bailey / lexbailey)

| Item | Location |
|------|----------|
| VHDL FPGA core | `scripts/upstream/ssem-inspired/c88/C88` — [lexbailey/C88](https://github.com/lexbailey/C88) |
| JS GUI emulator | `scripts/upstream/ssem-inspired/c88/c88-js` — [aquila12/c88-js](https://github.com/aquila12/c88-js) (no bundled demos; manual bit entry) |
| Extracted RAM images | `ssem-inspired/c88/c88_test_*.c88ram` |

Architecture: **8-bit words, 8-byte RAM**, GPIO, LED matrix — a scaled-down SSEM-*like*
homebrew CPU, not a Manchester Baby clone. Demo programs live in VHDL test benches
(`test_program_1.vhd` … `test_program_6_jma.vhd`).

Regenerate:

```bash
cd scripts
./download_upstream.sh   # clones C88 + c88-js
python3 convert_round5.py
```

## EMF Manchester Baby (Steven Goodwin)

| Item | Location |
|------|----------|
| Cached page + JS | `scripts/upstream/emf-manchester/` |
| Live URL | [em.ulat.es/machines/ManchesterBaby/](https://em.ulat.es/machines/ManchesterBaby/) |

The UI offers **Factor**, **Slide9**, **Noodle timer**, **Nightmare** (`.bys` / `.snp`
via `baby-importer.js`, LSB-first binary lines — same convention as many Baby SNPs).
Bundled `.bys` files were **not** downloadable from the live host (404) or Wayback
(404) in this round; they are almost certainly the David Sharp / competition family
already in `programs/davidsharp_*.store` and `davidsharp_baby9.store`.

## JsSSEM

Already converted into main catalog from Wayback `jsssem.html` (`convert_program_hunt.py`).
No additional unique tapes found in round 5.

## BabyBaby slider graphics (Boats / Trains / Christmas)

Published [g4ugm/BabyBaby](https://github.com/g4ugm/BabyBaby) `Programs.coe` ships three
banks only: **BabySlide (BABY)**, **PrimeGen**, **Diffeq** → `babybaby_slider_baby.store`,
`babybaby_primegen.store`, `babybaby_diffeqt.store`.

Hackaday / MSI mentions alternate slider bitmaps (**Boats**, **Trains**, **Christmas
Trees**). Those patterns were **not** found in the public GitHub tree (`Programs.coe`,
`squares.vhd`, `programs.xlsx`). They may exist only in museum builds or unpublished
Hackaday project files.

## Open SIMH SSEM

`scripts/upstream/open-simh/simh/SSEM/` implements LOAD/DUMP for **`.st`** store files
(`ssem_sys.c`). The repository ships **no sample `.st` programs** — only the simulator
sources.

## Baby8 (Jecel Assumpção)

Modern **8-bit CISC** soft-core named in honour of the Baby; **not** SSEM-compatible.
Reference only: [jeceljr/baby8](https://github.com/jeceljr/baby8). Optional cache:
`scripts/upstream/baby8-inspired/baby8` via `download_upstream.sh`.
