# Layer 8 harvest

Run after `./download_upstream.sh` (Madrona pages are also fetched by `convert_round10.py` via curl if missing).

```bash
cd MADM.English/scripts
python3 convert_round10.py
```

## 1. Madrona SSEM (`madrona.ca/e/SSEM`)

Cached: `scripts/upstream/madrona-ssem/programs/*.html` (curl `-k` — site cert mismatch).

Mirrors: `reference/madrona/programs/`.

| Program | Catalog |
|---------|---------|
| add, dtn, div, hcf, hf, bcdiv, primes, parabola, nightmare | dup existing David Sharp / NevynUK / emuStudio stores |
| **medclock** | **NEW** `madrona_medclock.store` (line 27 = fast-sim timing vs `davidsharp_medclock`) |
| **noodle** | **NEW** `madrona_noodletimer.store` (line 31 fast-sim vs `davidsharp_noodletimer`) |
| **sqrt** | **NEW** `madrona_sqrt.store` (Brent Hilpert 2000; JMP target line 26 = 4 vs emuStudio 5) |
| hf | dup `nevynuk_hcf1` (Tootill notebook X=35); **not** `kilburn_july48` (2^18) |

`lddiv.asm` in babyutils cites Madrona `div.html` (same as `nevynuk_turing_longdiv`).

## 2. Computer50 `ssemref.html`

`reference/manchester-ref/ssemref.html` + pattern `.asm` files.

| Pattern | Store |
|---------|-------|
| A2.1 add x+y | **NEW** `manchester_ref_add_xy.store` |
| A2.2 dec loop | **NEW** `manchester_ref_dec_loop_a22.store` (related to `emustudio_dec_till_negative`, different layout) |
| A2.3 instruction modification | reference only (incomplete fragment) |

## 3. HASE mirrors

`homepages.inf.ed.ac.uk/rni/hase/models/mu_baby/` — wget often blocked/slow; primary zip already in `scripts/upstream/hase/`. See `reference/hase_mirror_note.md`.

## 4. Oxford 8-bit SSEM

`scripts/upstream/oxford-8bit/manchesterSSEM8bit.js` — Elm UI, empty `Array.repeat 32 0`; **not** 32-bit Baby. Tracked under `ssem-inspired/oxford-8bit/` (reference only).

## 5. Digital60 `babyInstructions.html`

Instruction table + pedagogy; “first program below” points to other D60 pages, not a full listing here. Cached: `scripts/upstream/digital60-instructions/`. See `reference/digital60_baby_instructions_note.md`.

## New `.store` count

Up to **5** new files from `convert_round10.py` (skip if already present).
